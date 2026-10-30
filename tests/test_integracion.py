import json
import subprocess
import sys
from pathlib import Path
import numpy as np
import pytest
import soundfile as sf
from transcriptor.audio import convertir
from transcriptor.hablantes import diarizar


def audio_sintetico():
    """Dos timbres armónicos con envolventes; no son grabaciones humanas."""
    sr = 16000
    t = np.arange(sr * 6) / sr
    muestras = []
    for f0, formantes in [(110, [650, 1100, 2400]), (215, [350, 2200, 3100])]:
        voz = np.zeros_like(t)
        for armonico in range(1, 50):
            f = f0 * armonico
            amplitud = sum(np.exp(-0.5 * ((f - formante) / 170) ** 2) for formante in formantes)
            voz += amplitud / np.sqrt(armonico) * np.sin(2 * np.pi * f * t)
        envolvente = (0.25 + 0.75 * np.sin(np.pi * 3 * t) ** 2)
        voz = voz / np.max(np.abs(voz)) * 0.7 * envolvente
        muestras.extend([voz.astype("float32"), np.zeros(sr, dtype="float32")])
    return np.concatenate(muestras)


def test_dos_voces_sinteticas_ffmpeg_vad_huellas(tmp_path):
    original = tmp_path / "sintetico.wav"
    sf.write(original, audio_sintetico(), 16000)
    convertir(original, tmp_path / "mono.wav")
    audio, sr = sf.read(tmp_path / "mono.wav", dtype="float32")
    resultado = diarizar(audio, numero=2)
    assert sr == 16000
    assert {v["speaker"] for v in resultado["windows"]} == {"Hablante 1", "Hablante 2"}
    primera = [v["speaker"] for v in resultado["windows"] if v["end"] <= 6.1]
    segunda = [v["speaker"] for v in resultado["windows"] if v["start"] >= 7]
    assert primera and segunda and len(set(primera)) == len(set(segunda)) == 1
    assert primera[0] != segunda[0]
    automatico = diarizar(audio)
    assert {v["speaker"] for v in automatico["windows"]} == {"Hablante 1", "Hablante 2"}


def test_tiny_solo_si_esta_descargado(tmp_path):
    from transcriptor.asr import cargar_modelo
    try:
        modelo, _ = cargar_modelo("tiny", cpu=True)
    except ValueError:
        pytest.skip("Modelo tiny no descargado: no se accede a la red.")
    it, info = modelo.transcribe(audio_sintetico(), language="es", vad_filter=True, word_timestamps=True)
    assert isinstance(list(it), list)
    assert info.language == "es"


def test_cli_error_en_espanol():
    from transcriptor.__main__ import main
    assert main(["archivo_que_no_existe.wav"]) == 1


def test_video_rotulo_sintetico(tmp_path):
    import cv2
    from transcriptor.visual import leer_indicadores, resolver_nombres
    imagen = np.zeros((600, 900, 3), dtype="uint8")
    cv2.rectangle(imagen, (50, 50), (450, 350), (255, 140, 20), 3)
    cv2.putText(imagen, "Ana Prueba", (80, 320), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 255, 255), 2)
    ruta = tmp_path / "rotulo.mp4"
    escritor = cv2.VideoWriter(str(ruta), cv2.VideoWriter_fourcc(*"mp4v"), 5, (900, 600))
    assert escritor.isOpened()
    for _ in range(20):
        escritor.write(imagen)
    escritor.release()
    ventanas = [{"start": i, "end": i+1, "speaker": "Hablante 1"} for i in range(3)]
    evidencias = leer_indicadores(ruta, ventanas, tmp_path)
    assert len(evidencias) == 3
    assert resolver_nombres(ventanas, evidencias=evidencias)["Hablante 1"]["name"] == "Ana Prueba"
