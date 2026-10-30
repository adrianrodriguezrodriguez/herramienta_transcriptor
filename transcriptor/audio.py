from pathlib import Path
import shutil
import subprocess

EXTENSIONES = {".mp4", ".mkv", ".webm", ".mov", ".wav", ".mp3", ".m4a", ".ogg"}
VIDEOS = {".mp4", ".mkv", ".webm", ".mov"}


def convertir(origen: Path, destino: Path):
    if not origen.is_file():
        raise ValueError("El archivo de entrada no existe.")
    if origen.suffix.lower() not in EXTENSIONES:
        raise ValueError("Formato no admitido: " + origen.suffix)
    if not shutil.which("ffmpeg"):
        raise ValueError("Falta ffmpeg en PATH.")
    resultado = subprocess.run(
        ["ffmpeg", "-nostdin", "-v", "error", "-protocol_whitelist", "file,pipe", "-i", str(origen), "-vn", "-ac", "1",
         "-ar", "16000", "-c:a", "pcm_s16le", "-n", str(destino)],
        capture_output=True, text=True, encoding="utf-8", errors="replace",
    )
    if resultado.returncode:
        raise ValueError("ffmpeg no pudo extraer el audio: " + resultado.stderr.strip()[-1200:])
