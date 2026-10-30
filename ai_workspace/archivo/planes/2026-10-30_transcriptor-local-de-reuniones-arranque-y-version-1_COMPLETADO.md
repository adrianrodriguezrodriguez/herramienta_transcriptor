# Transcriptor local de reuniones — arranque y versión 1

> **Estado:** COMPLETADO
> Creado: 30/10/2026 por Claude. Lo ejecuta Codex. Proyecto: `C:\Proyectos\ia\herramienta_transcriptor`.

## Avance

- [x] Bloque 0 — Arranque (30/10/2026)
- [x] Bloque 1 — Versión 1 (30/10/2026)
- [x] Pruebas: 22 correctas, 1 omitida (30/10/2026)
- [x] Bloque 2 — Cierre: README, origen retirado, commit y push a GitHub (30/10/2026)

## Qué es

Programa local para Windows: se le da un vídeo o un audio y devuelve la transcripción con marcas de
tiempo y hablantes.
- **Hablantes:** se separan por voz (Hablante 1, 2…).
- **Nombres:** en grabaciones de Meet o Teams, se ponen solo cuando hay evidencia (rótulo en pantalla, indicador de quién habla o nombres que da el usuario). **Nunca reconocimiento facial.**
- **Privacidad:** todo en local; nada se sube a servicios externos.

## AUTORIZACIÓN (sin preguntar)

Autorizado:
- `git init` y commits locales (sin remoto: el usuario lo creará en su cuenta de empresa).
- Instalar AI Workspace 2.4.0 con las respuestas de abajo.
- Crear `.venv` e instalar paquetes de PyPI.
- Mover los modelos y copiar los scripts del origen.
- Al final, enviar a la Papelera la carpeta de origen.

Solo se para si algo amenaza datos del usuario o falta algo imprescindible.

## Origen reutilizable (verificado 30/10)

`C:\Users\iovip\.codex\tmp\io_066_auditoria` (8 GB), restos de transcripciones anteriores de Codex:
- `modelos\whisper\models--Systran--faster-whisper-large-v3` (2,9 GB): **se mueve**, no se descarga otra vez.
- `entorno\` (5 GB, venv con torch 2.6.0+cu124, faster-whisper 1.2.1, ctranslate2 4.8.3): **no se reutiliza** (un venv no se mueve de sitio); sirve como lista de versiones que funcionaron.
- Scripts de referencia:
  - `transcribir.py` (faster-whisper).
  - `diarizar.py` (webrtcvad + resemblyzer + clustering aglomerativo con silhouette).
  - `leer_indicadores_meet.py` (lee del vídeo el indicador de quién habla).
  - `revisar_asr.py` (repaso de tramos dudosos).

  Copiar su lógica, **quitando rutas, nombres y datos del proyecto de origen**.
- `reunion_it_29_10\` (audio `.wav` y capturas de una reunión real): **no se copia**; va a la Papelera con el resto.

Equipo: NVIDIA RTX 3050 Ti Laptop (4 GB), driver 610.62; ffmpeg instalado; Python 3.11 disponible (3.14
también, pero usar **3.11**).

## Bloque 0 — Arranque

1. `C:\Proyectos\ia\herramienta_transcriptor` (solo debe estar este plan). `git init`; identidad local `Adrián
   Rodríguez Rodríguez <258766955+adrianrodriguezrodriguez@users.noreply.github.com>` (la de `C:\Proyectos\ia`).
   - `.gitignore`: `.venv/`, `modelos/`, `entrada/`, `salida/`, `__pycache__/`, `*.wav`, `*.mp4`, `*.mkv`, `*.webm`, `*.mp3`, `*.m4a`.
2. AI Workspace 2.4.0 desde `C:\Proyectos\ia\plantilla_ai_workspace` (`iniciar.md`, sin hacer sus
   preguntas; copia en `%TEMP%`, borrada al verificar; conservar este plan). Respuestas:
   - **Proyecto:** «Transcriptor local de reuniones: vídeo o audio → texto con tiempos y hablantes; nombres solo con evidencia; todo local». Autoría: Adrián Rodríguez Rodríguez.
   - **Tecnologías:** Windows 11; Python 3.11, faster-whisper, ctranslate2, torch CUDA 12.4, resemblyzer, webrtcvad, scikit-learn, ffmpeg.
   - **Verificación:** `.venv\Scripts\python -m pytest`.
   - **Reglas:**
     - Vídeo y audio se procesan en local; nunca se suben.
     - Nombres de hablantes solo con evidencia; sin reconocimiento facial.
     - Las grabaciones del usuario no se modifican ni se copian al repo.
   - **Intocables:** `entrada/` (originales del usuario).
   - **Avisos:** `fases`. Modelo y esfuerzo: `medio_alto`. Asistentes: Claude y Codex. Graphify: sí. Interfaz: no.
3. `py -3.11 -m venv .venv`; instalar las versiones del entorno de origen (torch `2.6.0+cu124` desde el índice
   de PyTorch, faster-whisper 1.2.1, ctranslate2 4.8.3) más resemblyzer, webrtcvad-wheels, soundfile,
   scikit-learn, numpy, pytest. Fijarlas en `requirements.txt`. Comprobar `torch.cuda.is_available()`.
4. Mover `...\modelos\whisper\models--Systran--faster-whisper-large-v3` a `C:\Proyectos\ia\herramienta_transcriptor\modelos\whisper\`.
   Comprobar que carga desde ahí.

## Bloque 1 — Versión 1

Paquete `transcriptor/` y uso por consola:

```text
.venv\Scripts\python -m transcriptor <archivo> [--idioma es] [--hablantes N] [--nombres "Ana,David"] [--modelo large-v3|medium|small] [--cpu]
```

1. **Audio:** ffmpeg → WAV 16 kHz mono en una carpeta temporal. Acepta mp4, mkv, webm, mov, wav, mp3, m4a y ogg.
2. **Transcripción:** faster-whisper large-v3 en GPU (`int8_float16` para caber en 4 GB), con VAD y marcas por palabra. Si no hay GPU o con `--cpu`: `int8` y aviso de que será lento. Idioma automático si no se indica.
3. **Hablantes:** VAD, huellas de voz con resemblyzer, clustering; número automático (silhouette) o `--hablantes`. Cada tramo de texto se asigna al hablante con más solapamiento.
4. **Nombres:**
   - Con `--nombres`, se proponen por orden de primera intervención y el informe pide revisarlos.
   - Si es vídeo de Meet o Teams, con la lógica de `leer_indicadores_meet.py` (indicador de quién habla y rótulo con el nombre), solo cuando coincida con un tramo de voz.
   - Sin evidencia: «Hablante N». Nunca caras.
5. **Salida** en `salida/<nombre>_<fecha>/`:
   - `transcripcion.md`: `[hh:mm:ss] Nombre: texto`, con cabecera de duración, modelo, idioma, hablantes y de dónde sale cada nombre.
   - `transcripcion.srt` y `transcripcion.json` (tramos, palabras, confianza).
   - `revisar.md`: tramos de baja confianza y solapes.
6. **Progreso:** visible en consola (fase, % y tiempo estimado). Un fallo deja un mensaje claro en español.
7. **Comando `cerrar` del AI Workspace:** ninguno; el programa no envía nada a ningún sitio.

## Pruebas (pytest)

- **Unidad:** conversión de tiempos, unión de tramos, asignación de hablantes y escritura de md, srt y json.
- **Integración sin red:** audio sintético de dos «voces» distintas (tonos o ruido de distinto espectro, generado en la prueba) → 2 hablantes; modelo `tiny` solo si ya está descargado (si no, la prueba se salta y lo dice).
- **Prueba real:** el usuario pondrá una grabación propia en `entrada/`. Codex no usa grabaciones reales.

## Bloque 2 — Cierre

1. Pruebas OK. `README.md` corto: instalación, uso, salidas y límites (calidad de los nombres, GPU de 4 GB).
2. Enviar a la Papelera `C:\Users\iovip\.codex\tmp\io_066_auditoria` (ya sin los modelos, movidos en el bloque 0.4). Comprobar que no queda.
3. `ai_workspace\ESTADO.md` con lo hecho y lo pendiente; commit local «Transcriptor 1.0».
4. Informe al usuario en pocas líneas: qué funciona, cómo usarlo y espacio liberado.

## Riesgos

- **`resemblyzer` no instala en Python 3.11:** usar la versión que funcionó en el entorno de origen (consultar `entorno\Lib\site-packages`). Alternativa: SpeechBrain ECAPA. Lo que se elija va a `ESTADO.md`.
- **Memoria de la GPU:** si large-v3 no cabe, usar `medium` y avisar.
- **pyannote:** mejor separación, pero exige token de Hugging Face y aceptar licencias. Queda como mejora opcional, no en la v1.
