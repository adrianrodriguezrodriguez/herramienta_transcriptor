from pathlib import Path
import gc
import os

RAIZ = Path(__file__).resolve().parents[1]
_DLL_HANDLES = []


def localizar_modelo(nombre):
    from huggingface_hub import snapshot_download
    try:
        return Path(snapshot_download(f"Systran/faster-whisper-{nombre}",
                                     cache_dir=str(RAIZ / "modelos/whisper"), local_files_only=True,
                                     allow_patterns=["config.json", "model.bin", "tokenizer.json",
                                                     "vocabulary.*", "preprocessor_config.json"]))
    except Exception as exc:
        raise ValueError(f"El modelo {nombre} no está instalado en modelos/whisper. "
                         "Consulta README.md para descargarlo sin procesar grabaciones.") from exc


def cargar_modelo(nombre, cpu=False):
    import torch
    if os.name == "nt":
        _DLL_HANDLES.append(os.add_dll_directory(str(Path(torch.__file__).parent / "lib")))
    from faster_whisper import WhisperModel
    dispositivo = "cuda" if not cpu and torch.cuda.is_available() else "cpu"
    precision = "int8_float16" if dispositivo == "cuda" else "int8"
    if dispositivo == "cpu":
        print("Aviso: transcripción en CPU; puede ser lenta.", flush=True)
    ruta = localizar_modelo(nombre)
    modelo = WhisperModel(str(ruta), device=dispositivo, compute_type=precision,
                          cpu_threads=6, num_workers=1, local_files_only=True)
    return modelo, {"model": nombre, "device": dispositivo, "compute_type": precision}


def fila(segmento, offset=0):
    palabras = [{"start": p.start + offset, "end": p.end + offset, "word": p.word,
                 "probability": p.probability} for p in (segmento.words or [])]
    return {"start": segmento.start + offset, "end": segmento.end + offset,
            "text": segmento.text.strip(), "avg_logprob": segmento.avg_logprob,
            "no_speech_prob": segmento.no_speech_prob, "compression_ratio": segmento.compression_ratio,
            "confidence": sum(p["probability"] for p in palabras) / len(palabras) if palabras else None,
            "words": palabras}


def dudas(segmento):
    motivos = []
    if segmento.get("avg_logprob", 0) < -0.8:
        motivos.append("confianza ASR baja")
    if segmento.get("no_speech_prob", 0) > 0.6:
        motivos.append("posible ausencia de voz")
    if segmento.get("compression_ratio", 0) > 2.4:
        motivos.append("posible repetición artificial")
    if any(p["probability"] < 0.5 for p in segmento.get("words", [])):
        motivos.append("palabras de baja confianza")
    return motivos


def transcribir(audio, nombre="large-v3", idioma=None, cpu=False, progreso=lambda a, t: None):
    from .hablantes import unir_tramos
    def recuperar_memoria():
        gc.collect()
        import torch
        if torch.cuda.is_available():
            torch.cuda.empty_cache()

    def alternativa(actual):
        recuperar_memoria()
        if actual == "large-v3":
            try:
                localizar_modelo("medium")
                print("Aviso: large-v3 no cabe; se usará medium local.", flush=True)
                return cargar_modelo("medium", cpu)
            except ValueError:
                recuperar_memoria()
            except RuntimeError as exc:
                if not es_memoria(exc):
                    raise
                exc.__traceback__ = None
                recuperar_memoria()
        print("Aviso: memoria GPU insuficiente; se usará el modelo en CPU.", flush=True)
        return cargar_modelo(nombre, True)

    def es_memoria(exc):
        return any(t in str(exc).lower() for t in ("out of memory", "failed to alloc", "cuda_error_out_of_memory"))

    try:
        modelo, meta = cargar_modelo(nombre, cpu)
    except RuntimeError as exc:
        if cpu or not es_memoria(exc):
            raise
        exc.__traceback__ = None
        modelo, meta = alternativa(nombre)
    def ejecutar():
        iterador, info = modelo.transcribe(audio, language=idioma, beam_size=5, word_timestamps=True,
                                          vad_filter=True, vad_parameters={"min_silence_duration_ms": 500})
        segmentos = []
        for segmento in iterador:
            segmentos.append(fila(segmento))
            progreso(segmento.end, len(audio) / 16000)
        # Repasar solo tramos dudosos, sin vocabulario ni nombres del origen.
        revisiones = []
        for inicio, fin in unir_tramos([(s["start"], s["end"]) for s in segmentos if dudas(s)], margen=0):
            anteriores = [s for s in segmentos if s["end"] > inicio and s["start"] < fin]
            it, _ = modelo.transcribe(audio[int(inicio * 16000):int(fin * 16000)],
                                     language=idioma or info.language, beam_size=5, word_timestamps=True,
                                     vad_filter=True, condition_on_previous_text=False,
                                     hallucination_silence_threshold=1.5)
            nuevas = [fila(s, inicio) for s in it]
            mejor = nuevas and sum(s["avg_logprob"] for s in nuevas) / len(nuevas) > sum(s["avg_logprob"] for s in anteriores) / len(anteriores)
            revisiones.append({"start": inicio, "end": fin, "accepted": bool(mejor)})
            if mejor:
                segmentos = [s for s in segmentos if s not in anteriores] + nuevas
        return segmentos, info, revisiones

    while True:
        try:
            segmentos, info, revisiones = ejecutar()
            break
        except RuntimeError as exc:
            if meta["device"] != "cuda" or not es_memoria(exc):
                raise
            # Soltar también los iteradores retenidos por la traza antes de recargar.
            exc.__traceback__ = None
            del modelo
            modelo, meta = alternativa(meta["model"])
    segmentos.sort(key=lambda s: s["start"])
    meta.update(language=info.language, language_probability=info.language_probability,
                duration=len(audio) / 16000, revisions=revisiones)
    progreso(1, 1)
    return segmentos, meta
