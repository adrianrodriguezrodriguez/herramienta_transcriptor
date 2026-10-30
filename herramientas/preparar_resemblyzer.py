"""Empaqueta Resemblyzer 0.1.4 con dependencias compatibles con Python 3.11.

No cambia código ni pesos: sustituye la dependencia webrtcvad por su wheel
equivalente y retira typing (incluido en Python). Conserva licencias y RECORD.
Ejecutar después de instalar el wheel oficial con --no-deps.
"""
import base64
import csv
import hashlib
import importlib.metadata
import io
from pathlib import Path
import zipfile


def main():
    distribucion = importlib.metadata.distribution("Resemblyzer")
    if distribucion.version != "0.1.4":
        raise SystemExit("Se requiere el paquete oficial Resemblyzer 0.1.4.")
    version = "0.1.4+vadwheels"
    carpeta = f"Resemblyzer-{version}.dist-info"
    destino = Path(__file__).resolve().parents[1] / "dependencias" / f"Resemblyzer-{version}-py3-none-any.whl"
    destino.parent.mkdir(exist_ok=True)
    contenido = {}
    for archivo in distribucion.files:
        nombre = archivo.as_posix()
        if nombre.startswith("resemblyzer/") and "__pycache__" not in nombre:
            contenido[nombre] = Path(distribucion.locate_file(archivo)).read_bytes()
        elif ".dist-info/" in nombre and nombre.rsplit("/", 1)[-1] in {"METADATA", "WHEEL", "LICENSE", "LICENSE.txt", "top_level.txt"}:
            datos = Path(distribucion.locate_file(archivo)).read_bytes()
            if nombre.endswith("/METADATA"):
                texto = datos.decode("utf-8").replace("\r\n", "\n").replace("Version: 0.1.4\n", f"Version: {version}\n")
                lineas = []
                for linea in texto.splitlines():
                    if linea.startswith("Requires-Dist: webrtcvad ") or linea.startswith("Requires-Dist: webrtcvad>"):
                        linea = "Requires-Dist: webrtcvad-wheels==2.0.14.post1"
                    if linea == "Requires-Dist: typing":
                        continue
                    lineas.append(linea)
                datos = ("\n".join(lineas) + "\n").encode("utf-8")
            contenido[f"{carpeta}/{nombre.rsplit('/', 1)[-1]}"] = datos
    if not any(n.endswith("pretrained.pt") for n in contenido):
        raise SystemExit("Faltan los pesos del paquete oficial.")
    registro = io.StringIO(newline="")
    escritor = csv.writer(registro, lineterminator="\n")
    for nombre, datos in contenido.items():
        digest = base64.urlsafe_b64encode(hashlib.sha256(datos).digest()).rstrip(b"=").decode()
        escritor.writerow([nombre, "sha256=" + digest, len(datos)])
    escritor.writerow([f"{carpeta}/RECORD", "", ""])
    contenido[f"{carpeta}/RECORD"] = registro.getvalue().encode()
    with zipfile.ZipFile(destino, "w", zipfile.ZIP_DEFLATED) as wheel:
        for nombre, datos in contenido.items():
            wheel.writestr(nombre, datos)
    print(destino)


if __name__ == "__main__":
    main()
