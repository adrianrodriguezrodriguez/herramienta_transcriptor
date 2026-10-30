import argparse
from datetime import datetime
from pathlib import Path
import sys
import tempfile
import time

from .audio import convertir, VIDEOS
from .asr import RAIZ, transcribir
from .hablantes import diarizar, asignar
from .progreso import Progreso
from .salida import escribir
from .visual import leer_indicadores, resolver_nombres


def parser():
    p = argparse.ArgumentParser(description="Transcriptor local de audio y vídeo con tiempos y hablantes.")
    p.add_argument("archivo", type=Path)
    p.add_argument("--idioma", default=None, help="Código del idioma; automático por defecto")
    p.add_argument("--hablantes", type=int)
    p.add_argument("--nombres", help='Nombres por orden de intervención, p. ej. "Ana,David"; revisar siempre')
    p.add_argument("--modelo", choices=("large-v3", "medium", "small"), default="large-v3")
    p.add_argument("--cpu", action="store_true")
    return p


def main(argv=None):
    for flujo in (sys.stdout, sys.stderr):
        if hasattr(flujo, "reconfigure"):
            flujo.reconfigure(encoding="utf-8")
    args = parser().parse_args(argv)
    if args.hablantes is not None and args.hablantes < 1:
        parser().error("--hablantes debe ser mayor que cero")
    nombres = [n.strip() for n in args.nombres.split(",")] if args.nombres else None
    if nombres and (any(not n for n in nombres) or len(set(nombres)) != len(nombres)):
        parser().error("Los nombres deben ser distintos y no estar vacíos")
    inicio = time.monotonic()
    try:
        import soundfile as sf
        import numpy as np
        with tempfile.TemporaryDirectory(prefix="transcriptor_") as carpeta:
            temporal = Path(carpeta)
            progreso = Progreso("Conversión de audio")
            convertir(args.archivo.resolve(), temporal / "audio.wav")
            audio, sr = sf.read(temporal / "audio.wav", dtype="float32")
            if sr != 16000 or not len(audio):
                raise ValueError("El archivo no contiene audio utilizable.")
            progreso(1, 1)
            segmentos, meta = transcribir(np.asarray(audio), args.modelo, args.idioma, args.cpu, Progreso("Transcripción y revisión"))
            # El modelo ASR queda fuera de alcance antes de calcular las huellas.
            diarizacion = diarizar(audio, args.hablantes, Progreso("Separación de voces"))
            asignar(segmentos, diarizacion["windows"])
            evidencias, avisos = [], []
            if args.archivo.suffix.lower() in VIDEOS and not nombres:
                try:
                    evidencias = leer_indicadores(args.archivo.resolve(), diarizacion["windows"], temporal, Progreso("Rótulos del vídeo"))
                except (ValueError, OSError, TimeoutError) as exc:
                    avisos.append(str(exc))
                    print(f"Aviso: {exc}. Se conservarán identificadores de hablante.", flush=True)
            mapa = resolver_nombres(diarizacion["windows"], nombres, evidencias)
            if not segmentos:
                avisos.append("No se obtuvo texto; el audio puede no contener voz inteligible.")
            meta.update(elapsed_seconds=round(time.monotonic() - inicio, 2), warnings=avisos)
            destino = RAIZ / "salida" / f"{args.archivo.stem}_{datetime.now():%Y%m%d_%H%M%S_%f}"
            escribir(destino, segmentos, meta, mapa, diarizacion, evidencias)
        print(f"Terminado. Resultados: {destino}")
        return 0
    except KeyboardInterrupt:
        print("\nProceso cancelado. El original sigue intacto.", file=sys.stderr)
        return 130
    except Exception as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
