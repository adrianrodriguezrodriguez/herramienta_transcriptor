"""VAD WebRTC, huellas Resemblyzer y agrupación por similitud acústica."""
import numpy as np


def unir_tramos(tramos, margen=0.24):
    unidos = []
    for inicio, fin in sorted(tramos):
        if unidos and inicio - unidos[-1][1] <= margen:
            unidos[-1][1] = max(fin, unidos[-1][1])
        else:
            unidos.append([float(inicio), float(fin)])
    return unidos


def regiones_voz(audio, sr=16000):
    import webrtcvad
    vad = webrtcvad.Vad(2)
    pcm = (np.clip(audio, -1, 1) * 32767).astype("<i2")
    tam = int(sr * 0.03)
    activos = [(p / sr, (p + tam) / sr) for p in range(0, len(pcm) - tam + 1, tam)
               if vad.is_speech(pcm[p:p + tam].tobytes(), sr)]
    return [r for r in unir_tramos(activos) if r[1] - r[0] >= 0.18]


def agrupar(vectores, numero=None):
    from sklearn.cluster import AgglomerativeClustering
    from sklearn.metrics import silhouette_score
    cantidad = len(vectores)
    if numero is not None and (numero < 1 or numero > cantidad):
        raise ValueError(f"Se pidieron {numero} hablantes y solo hay {cantidad} ventanas de voz.")
    if cantidad < 2 or numero == 1:
        return np.zeros(cantidad, dtype=int), []
    def etiquetas(k):
        return AgglomerativeClustering(n_clusters=k, metric="cosine", linkage="average").fit_predict(vectores)
    if numero:
        return etiquetas(numero), []
    normalizados = vectores / np.maximum(np.linalg.norm(vectores, axis=1, keepdims=True), 1e-10)
    distancia = 1 - normalizados @ normalizados.T
    if float(np.max(distancia)) < 0.18:
        return np.zeros(cantidad, dtype=int), []
    candidatos = []
    for k in range(2, min(8, cantidad - 1) + 1):
        grupos = etiquetas(k)
        valor = float(silhouette_score(vectores, grupos, metric="cosine"))
        candidatos.append({"k": k, "silhouette": valor})
    if not candidatos:
        return (etiquetas(2) if float(np.max(distancia)) >= 0.3 else np.zeros(cantidad, dtype=int)), []
    mejor = max(candidatos, key=lambda c: c["silhouette"])
    return (etiquetas(mejor["k"]) if mejor["silhouette"] >= 0.35 else np.zeros(cantidad, dtype=int)), candidatos


def diarizar(audio, numero=None, progreso=lambda a, t: None):
    import torch
    from resemblyzer import VoiceEncoder
    from resemblyzer.audio import normalize_volume
    torch.set_num_threads(4)
    regiones = regiones_voz(audio)
    ventanas = []
    for inicio, fin in regiones:
        pos = inicio
        while pos < fin:
            final = min(pos + 3, fin)
            ventanas.append({"start": pos, "end": final})
            if final == fin:
                break
            pos += 2
    if not ventanas:
        if numero:
            raise ValueError("No se detectó voz para el número de hablantes solicitado.")
        progreso(1, 1)
        return {"windows": [], "candidates": [], "regions": []}
    encoder = VoiceEncoder(device="cpu", verbose=False)
    vectores = []
    for i, ventana in enumerate(ventanas):
        clip = audio[int(ventana["start"] * 16000):int(ventana["end"] * 16000)]
        # No se recorta con otro VAD: conservar también las intervenciones breves.
        clip = normalize_volume(clip, -30, increase_only=True)
        if len(clip) < 16000:
            clip = np.pad(clip, (0, 16000 - len(clip)))
        vectores.append(encoder.embed_utterance(clip))
        progreso(i + 1, len(ventanas))
    etiquetas, candidatos = agrupar(np.asarray(vectores), numero)
    orden = {}
    for ventana, etiqueta in zip(ventanas, etiquetas):
        if int(etiqueta) not in orden:
            orden[int(etiqueta)] = f"Hablante {len(orden) + 1}"
        ventana["speaker"] = orden[int(etiqueta)]
    return {"windows": ventanas, "regions": regiones, "candidates": candidatos}


def asignar(segmentos, ventanas):
    for segmento in segmentos:
        duraciones = {}
        for ventana in ventanas:
            inicio = max(segmento["start"], ventana["start"])
            fin = min(segmento["end"], ventana["end"])
            if fin > inicio:
                duraciones.setdefault(ventana["speaker"], []).append((inicio, fin))
        pesos = {voz: sum(b - a for a, b in unir_tramos(tramos, margen=0))
                 for voz, tramos in duraciones.items()}
        segmento["speaker"] = max(pesos, key=pesos.get) if pesos else "Hablante sin determinar"
        # Es una posible mezcla de voces, no prueba de habla simultánea.
        segmento["possible_overlap"] = len(pesos) > 1 and min(pesos.values()) >= 0.2
    return segmentos
