"""Solo bordes activos y rótulos; nunca inspecciona ni reconoce rostros."""
from collections import Counter, defaultdict
from pathlib import Path
import json
import subprocess
import re


def recortes_rotulos(imagen):
    import cv2
    import numpy as np
    hsv = cv2.cvtColor(imagen, cv2.COLOR_BGR2HSV)
    # Bordes de actividad verde/azul/violeta habituales en Meet y Teams.
    mascara = cv2.inRange(hsv, np.array([35, 65, 100]), np.array([165, 255, 255]))
    contornos, _ = cv2.findContours(mascara, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    alto, ancho = imagen.shape[:2]
    candidatos = []
    for contorno in contornos:
        x, y, w, h = cv2.boundingRect(contorno)
        if w < 100 or h < 60 or w > ancho * 0.98 or h > alto * 0.98:
            continue
        franja = mascara[y:y+h, x:x+w] > 0
        bordes = [franja[:4].max(axis=0).mean(), franja[-4:].max(axis=0).mean(),
                  franja[:, :4].max(axis=1).mean(), franja[:, -4:].max(axis=1).mean()]
        if min(bordes) < 0.65:
            continue
        # Solo se envía al OCR la franja inferior donde aparece el rótulo.
        candidatos.append(imagen[y + int(h * 0.72):y + h - 3, x + 3:x + w - 3])
    return candidatos


def ocr(imagen, temporal):
    import cv2
    ruta = temporal / "rotulo.png"
    cv2.imwrite(str(ruta), cv2.resize(imagen, None, fx=2, fy=2))
    try:
        resultado = subprocess.run(
            ["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-File",
             str(Path(__file__).with_name("ocr_windows.ps1")), "-Imagen", str(ruta)],
            capture_output=True, encoding="utf-8", errors="replace", timeout=30,
        )
    except subprocess.TimeoutExpired as exc:
        raise ValueError("El OCR local superó el tiempo de espera") from exc
    if resultado.returncode:
        raise ValueError("OCR local no disponible: " + resultado.stderr.strip()[-400:])
    lineas = json.loads(resultado.stdout)
    if isinstance(lineas, str):
        lineas = [lineas]
    # Abstenerse ante varios rótulos, iconos o texto ambiguo.
    nombres = [s.strip() for s in lineas if re.fullmatch(r"[^\W\d_][^\d\W_]*(?:[ .’'\-][^\W\d_]+){0,7}", s.strip(), re.UNICODE)]
    return nombres[0] if len(nombres) == 1 and 2 <= len(nombres[0]) <= 80 else None


def leer_indicadores(video, ventanas, temporal, progreso=lambda a, t: None):
    import cv2
    if not ventanas:
        return []
    captura = cv2.VideoCapture(str(video))
    if not captura.isOpened():
        raise ValueError("No se pudo abrir el vídeo para leer rótulos.")
    registros = []
    tiempos = sorted({round((v["start"] + v["end"]) / 2, 2) for v in ventanas})
    try:
        for i, instante in enumerate(tiempos):
            activas = {v["speaker"] for v in ventanas if v["start"] <= instante < v["end"]}
            if len(activas) == 1:
                captura.set(cv2.CAP_PROP_POS_MSEC, instante * 1000)
                ok, imagen = captura.read()
                if ok:
                    recortes = recortes_rotulos(imagen)
                    if len(recortes) == 1:
                        nombre = ocr(recortes[0], temporal)
                        if nombre:
                            registros.append({"time": instante, "speaker": next(iter(activas)),
                                              "name": nombre, "source": "rótulo OCR y borde activo coincidentes con voz"})
            progreso(i + 1, len(tiempos))
    finally:
        captura.release()
    return registros


def resolver_nombres(ventanas, propuestos=None, evidencias=()):
    voces = list(dict.fromkeys(v["speaker"] for v in sorted(ventanas, key=lambda v: v["start"])))
    resultado = {voz: {"name": voz, "source": "sin evidencia nominal"} for voz in voces}
    if propuestos:
        if len(propuestos) != len(voces):
            raise ValueError(f"Se recibieron {len(propuestos)} nombres para {len(voces)} voces; ajusta --hablantes y --nombres.")
        for voz, nombre in zip(voces, propuestos):
            resultado[voz] = {"name": nombre, "source": "propuesto por el usuario por orden de primera intervención; REVISAR"}
        return resultado
    votos = defaultdict(Counter)
    for evidencia in evidencias:
        # Una lectura OCR solo cuenta si cae dentro de una única voz detectada.
        activas = {v["speaker"] for v in ventanas if v["start"] <= evidencia["time"] < v["end"]}
        if activas == {evidencia["speaker"]}:
            votos[evidencia["speaker"]][evidencia["name"]] += 1
    candidatos = {}
    for voz, conteo in votos.items():
        nombre, cantidad = conteo.most_common(1)[0]
        if cantidad >= 3 and cantidad / conteo.total() >= 0.8:
            candidatos[voz] = nombre
    repetidos = Counter(candidatos.values())
    for voz, nombre in candidatos.items():
        if voz in resultado and repetidos[nombre] == 1:
            resultado[voz] = {"name": nombre, "source": "rótulo OCR y borde activo repetidos en ≥3 muestras con voz; REVISAR"}
    return resultado
