import json
import numpy as np
import pytest
from transcriptor.hablantes import unir_tramos, asignar, agrupar
from transcriptor.salida import tiempo, escribir
from transcriptor.visual import resolver_nombres, recortes_rotulos, ocr
from transcriptor.audio import convertir


def test_tiempos_y_redondeo():
    assert tiempo(3661.234, True) == "01:01:01,234"
    assert tiempo(59.9996, True) == "00:01:00,000"
    assert tiempo(-1) == "00:00:00"
    assert tiempo(360001) == "100:00:01"


def test_union_y_solapamiento():
    assert unir_tramos([(2, 4), (0, 1), (0.5, 0.8), (1.2, 2.1)]) == [[0., 4.]]
    ventanas = [{"start": 0, "end": 3, "speaker": "Hablante 1"},
                {"start": 2, "end": 4, "speaker": "Hablante 1"},
                {"start": 4, "end": 8.5, "speaker": "Hablante 2"}]
    segmentos = [{"start": 0, "end": 8.5}, {"start": 10, "end": 11}]
    asignar(segmentos, ventanas)
    assert segmentos[0]["speaker"] == "Hablante 2"  # no contar dos veces ventanas solapadas
    assert segmentos[0]["possible_overlap"]
    assert segmentos[1]["speaker"] == "Hablante sin determinar"


def test_agrupacion_casos_limite():
    assert agrupar(np.ones((1, 3)))[0].tolist() == [0]
    assert agrupar(np.ones((4, 3)))[0].tolist() == [0, 0, 0, 0]
    with pytest.raises(ValueError):
        agrupar(np.ones((1, 3)), 2)


def test_nombres_solo_con_evidencia_y_orden():
    ventanas = [{"start": 4, "end": 8, "speaker": "Hablante 2"},
                {"start": 0, "end": 4, "speaker": "Hablante 1"}]
    assert resolver_nombres(ventanas)["Hablante 1"]["name"] == "Hablante 1"
    assert resolver_nombres(ventanas, ["Ana", "David"])["Hablante 1"]["name"] == "Ana"
    with pytest.raises(ValueError):
        resolver_nombres(ventanas, ["Ana"])
    pruebas = [{"time": t, "speaker": "Hablante 1", "name": "Ana"} for t in [0.5, 1.5, 2.5]]
    assert resolver_nombres(ventanas, evidencias=pruebas)["Hablante 1"]["name"] == "Ana"
    assert resolver_nombres(ventanas, evidencias=pruebas[:1])["Hablante 1"]["name"] == "Hablante 1"
    sin_voz = [dict(e, time=20) for e in pruebas]
    assert resolver_nombres(ventanas, evidencias=sin_voz)["Hablante 1"]["name"] == "Hablante 1"


def test_escritura_tres_formatos_y_revision(tmp_path):
    segmentos = [{"start": 1.25, "end": 3, "speaker": "Hablante 1", "text": "Texto sintético.",
                  "avg_logprob": -1, "words": [{"start": 1.25, "end": 2, "word": "Texto", "probability": 0.3}],
                  "possible_overlap": True}]
    meta = {"duration": 5, "model": "simulado", "device": "cpu", "compute_type": "int8", "language": "es"}
    destino = tmp_path / "resultado"
    nombres = {"Hablante 1": {"name": "Ana", "source": "propuesta; REVISAR"}}
    escribir(destino, segmentos, meta, nombres, {}, [])
    assert "[00:00:01] Ana: Texto sintético." in (destino / "transcripcion.md").read_text(encoding="utf-8")
    assert "00:00:01,250 --> 00:00:03,000" in (destino / "transcripcion.srt").read_text(encoding="utf-8")
    assert json.loads((destino / "transcripcion.json").read_text(encoding="utf-8"))["segments"][0]["words"][0]["probability"] == 0.3
    revision = (destino / "revisar.md").read_text(encoding="utf-8")
    assert "baja" in revision and "solape" in revision and "REVISAR" in revision
    with pytest.raises(FileExistsError):
        escribir(destino, segmentos, meta, nombres, {}, [])


def test_original_no_se_modifica(tmp_path):
    import soundfile as sf
    archivo = tmp_path / "original.wav"
    sf.write(archivo, np.zeros(1600), 16000)
    antes = archivo.read_bytes()
    convertir(archivo, tmp_path / "convertido.wav")
    assert archivo.read_bytes() == antes
    datos, sr = sf.read(tmp_path / "convertido.wav")
    assert sr == 16000 and datos.ndim == 1


def imagen_sintetica():
    import cv2
    imagen = np.zeros((600, 900, 3), dtype=np.uint8)
    cv2.rectangle(imagen, (50, 50), (450, 350), (255, 140, 20), 3)
    cv2.putText(imagen, "Ana Prueba", (80, 320), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 255, 255), 2)
    return imagen


def test_indicador_solo_recorta_rotulo():
    recortes = recortes_rotulos(imagen_sintetica())
    assert len(recortes) == 1
    assert recortes[0].shape[0] < 100
    assert not recortes_rotulos(np.zeros((600, 900, 3), dtype=np.uint8))


def test_ocr_windows_sintetico(tmp_path):
    assert ocr(recortes_rotulos(imagen_sintetica())[0], tmp_path) == "Ana Prueba"


@pytest.mark.parametrize("caso", ["solape", "contradiccion", "nombre_repetido"])
def test_rotulos_ambiguos_no_asignan_nombres(caso):
    ventanas = [{"start": 0, "end": 5, "speaker": "Hablante 1"},
                {"start": 5, "end": 10, "speaker": "Hablante 2"}]
    pruebas = [{"time": t, "speaker": "Hablante 1", "name": "Ana"} for t in [1, 2, 3]]
    if caso == "solape":
        ventanas[1]["start"] = 0
    elif caso == "contradiccion":
        pruebas.append({"time": 4, "speaker": "Hablante 1", "name": "David"})
    else:
        pruebas.extend({"time": t, "speaker": "Hablante 2", "name": "Ana"} for t in [6, 7, 8])
    nombres = resolver_nombres(ventanas, evidencias=pruebas)
    assert all(datos["name"] == voz for voz, datos in nombres.items())


def test_ocr_agotado_permite_conservar_identificadores(monkeypatch, tmp_path):
    import subprocess
    def agotar(*args, **kwargs):
        raise subprocess.TimeoutExpired("powershell", 30)
    monkeypatch.setattr(subprocess, "run", agotar)
    with pytest.raises(ValueError, match="OCR local superó el tiempo"):
        ocr(recortes_rotulos(imagen_sintetica())[0], tmp_path)
