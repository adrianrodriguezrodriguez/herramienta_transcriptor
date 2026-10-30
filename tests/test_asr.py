from types import SimpleNamespace
import numpy as np
import pytest
from transcriptor import asr


def test_cache_local_solo_archivos_del_modelo(monkeypatch):
    import huggingface_hub
    def descargar(repo, **opciones):
        assert repo == "Systran/faster-whisper-large-v3"
        assert opciones["local_files_only"] is True
        assert "model.bin" in opciones["allow_patterns"]
        assert "README.md" not in opciones["allow_patterns"]
        return "modelo_local"
    monkeypatch.setattr(huggingface_hub, "snapshot_download", descargar)
    assert asr.localizar_modelo("large-v3").name == "modelo_local"


def test_falta_memoria_al_cargar_recurre_a_cpu(monkeypatch):
    llamadas = []
    class Modelo:
        def transcribe(self, audio, **kwargs):
            return iter([]), SimpleNamespace(language="es", language_probability=1)
    def cargar(nombre, cpu=False):
        llamadas.append((nombre, cpu))
        if not cpu:
            raise RuntimeError("CUDA out of memory")
        return Modelo(), {"model": nombre, "device": "cpu", "compute_type": "int8"}
    def sin_medium(nombre):
        raise ValueError("No instalado")
    monkeypatch.setattr(asr, "cargar_modelo", cargar)
    monkeypatch.setattr(asr, "localizar_modelo", sin_medium)
    segmentos, meta = asr.transcribir(np.zeros(16000, dtype="float32"))
    assert not segmentos
    assert llamadas == [("large-v3", False), ("large-v3", True)]
    assert meta["device"] == "cpu"


@pytest.mark.parametrize("fase", ["segmentos", "revision"])
@pytest.mark.parametrize("medium_local", [False, True])
def test_memoria_durante_proceso_reinicia_sin_duplicar(monkeypatch, fase, medium_local):
    llamadas = []
    segmento = SimpleNamespace(start=0, end=1, text="Texto", words=[],
                              avg_logprob=-1, no_speech_prob=0, compression_ratio=1)

    class Modelo:
        def __init__(self, nombre, cpu):
            self.nombre, self.cpu = nombre, cpu
            self.pasadas = 0

        def transcribe(self, audio, **kwargs):
            self.pasadas += 1
            fallar = not self.cpu and (fase == "segmentos" or self.pasadas == 2)

            def generar():
                yield segmento
                if fallar:
                    raise RuntimeError("CUDA out of memory")

            return generar(), SimpleNamespace(language="es", language_probability=1)

    def cargar(nombre, cpu=False):
        llamadas.append((nombre, cpu))
        return Modelo(nombre, cpu), {"model": nombre, "device": "cpu" if cpu else "cuda"}

    def localizar(nombre):
        if not medium_local:
            raise ValueError("No instalado")
        return nombre

    monkeypatch.setattr(asr, "cargar_modelo", cargar)
    monkeypatch.setattr(asr, "localizar_modelo", localizar)
    segmentos, meta = asr.transcribir(np.zeros(16000, dtype="float32"))
    assert len(segmentos) == 1
    assert meta["device"] == "cpu"
    assert llamadas == ([("large-v3", False), ("medium", False), ("large-v3", True)]
                        if medium_local else [("large-v3", False), ("large-v3", True)])


def test_error_ajeno_a_memoria_no_se_oculta(monkeypatch):
    def cargar(*args):
        raise RuntimeError("Modelo dañado")
    monkeypatch.setattr(asr, "cargar_modelo", cargar)
    with pytest.raises(RuntimeError, match="Modelo dañado"):
        asr.transcribir(np.zeros(16000, dtype="float32"))
