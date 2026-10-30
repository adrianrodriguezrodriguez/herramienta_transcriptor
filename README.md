# Transcriptor local de reuniones

Windows 11 y Python 3.11. Convierte audio o vídeo en texto con tiempos y voces,
sin subir grabaciones ni usar reconocimiento facial. Autor: Adrián Rodríguez Rodríguez.

## Instalación

El entorno `.venv` y large-v3 ya están instalados en este equipo. Para recrear
el entorno, instala Python 3.11 y ffmpeg en PATH y ejecuta:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\instalar.ps1
```

La instalación de paquetes necesita Internet; la transcripción funciona sin red.
`requirements.txt` fija versiones. El wheel local de Resemblyzer conserva el código,
pesos y licencia de 0.1.4: solo cambia `webrtcvad` por `webrtcvad-wheels` y retira
la dependencia obsoleta `typing`. `herramientas/preparar_resemblyzer.py` documenta
y reproduce ese empaquetado a partir del paquete oficial instalado sin dependencias.

## Uso

Desde esta carpeta, coloca tu archivo en `entrada/` o indica su ruta local:

```powershell
.venv\Scripts\python -m transcriptor "entrada\reunion.mp4" --idioma es
.venv\Scripts\python -m transcriptor "entrada\audio.wav" --hablantes 2 --nombres "Ana,David"
.venv\Scripts\python -m transcriptor "entrada\audio.wav" --cpu
```

Admite mp4, mkv, webm, mov, wav, mp3, m4a y ogg. Sin `--idioma`, lo detecta.
Los originales se leen; el WAV de trabajo se genera y elimina en una carpeta temporal.
No existe comando de envío, publicación o mensajería en el programa.

Cada ejecución crea `salida/<nombre>_<fecha>/` con `transcripcion.md`,
`transcripcion.srt`, `transcripcion.json` (palabras, confianza, evidencias y metadatos)
y `revisar.md` (baja confianza, nombres propuestos y posibles mezclas de voces).

## Modelos y límites

Large-v3 usa CUDA `int8_float16` para la GPU de 4 GB; en CPU usa `int8` y tarda más.
Si falta memoria al cargar, transcribir o repasar, se intenta medium local; si no
está o tampoco cabe, se utiliza el modelo solicitado en CPU. Se reinicia el proceso
sin duplicar segmentos. `--modelo medium` o `--modelo small` requieren instalarlos antes:

```powershell
.venv\Scripts\python -c "from huggingface_hub import snapshot_download; snapshot_download('Systran/faster-whisper-medium', cache_dir='modelos/whisper')"
```

Ese comando descarga únicamente un modelo, sin leer grabaciones. El programa nunca
descarga modelos automáticamente y avisa si falta uno.

La separación de voces y su número automático son aproximados. Usa `--hablantes N`
cuando conozcas el número. Voces superpuestas, intervenciones cortas y cambios de
micrófono pueden confundirse; los solapes se señalan como posibles, no confirmados.
Los tiempos y probabilidades proceden del ASR y no son alineación fonética ni certeza factual.

`--nombres` propone nombres por primera intervención y exige revisión humana.
En vídeos, el lector local busca bordes activos y rótulos de Meet/Teams mediante
OCR de Windows, sin analizar caras: exige varias lecturas coincidentes con voz.
Depende del diseño, idioma OCR instalado y resolución; ante duda conserva «Hablante N».
Revisa siempre las atribuciones nominales, también las obtenidas por OCR.

## Verificación

```powershell
.venv\Scripts\python -m pytest
```

Solo usa audio e imágenes sintéticos. Las conexiones de red de Python están bloqueadas
en las pruebas. La prueba ASR con tiny se omite explícitamente si no está descargado.
No se utilizan las grabaciones de los usuarios.

AI Workspace 2.4.0 incluye configuración para Claude y Codex y mapa Graphify local.
Para actualizar el mapa en entornos restringidos:

```powershell
$env:GRAPHIFY_MAX_WORKERS='1'
graphify update .
```

Los hooks de Codex solo se ejecutan cuando el usuario los confía en `/hooks`.
`PLAN_ACTUAL.md` se conserva; el cierre efectivo figura en `ai_workspace/ESTADO.md`.
