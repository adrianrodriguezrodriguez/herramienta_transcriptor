---
name: transcribir-reunion
description: Transcribe una reunión con herramientas locales, tiempos y nombres de hablantes solo con evidencia.
---

1. Localiza la raíz que contiene transcriptor/__main__.py. Lee AGENTS.md y README.md y comprueba el entorno .venv, ffmpeg y los modelos locales existentes. No instales dependencias ni descargues modelos automáticamente.
2. Investiga el archivo y lo ya indicado antes de preguntar. Máximo cinco preguntas numeradas por mensaje, cortas, de sí/no o elegir: qué archivo local; idioma automático o uno indicado; número conocido de voces o estimación; conservar Hablante N o nombres con evidencia; salida habitual o ubicación autorizada. Reutiliza respuestas confirmadas. No inventes rutas, idiomas ni identidades.
3. Ejecuta desde la herramienta .venv/Scripts/python.exe -B -m transcriptor <archivo> y solo las opciones verificadas necesarias: --idioma, --hablantes, --modelo o --cpu. La salida habitual se crea en salida/<nombre>_<fecha>. Para otra ubicación comprueba primero que el programa lo admite; no inventes una opción --salida. Conserva los originales fuera del repositorio y no los modifiques ni copies dentro.
4. Todo el audio, vídeo, reconocimiento y revisión se procesa localmente; nunca subas una grabación, fragmento o transcripción a un servicio externo. No uses reconocimiento facial. Si falta un modelo o un recurso, informa y espera una decisión antes de descargar o instalar algo.
5. Mantén Hablante N si no hay evidencia de identidad. --nombres solo se usa con correspondencia confirmada entre persona y orden de intervención; una lista de nombres por sí sola no prueba quién habló. Los rótulos de reunión obtenidos por OCR local requieren varias lecturas concordantes y revisión humana; anota qué evidencia respalda cada nombre. Marca como inciertos los solapes, palabras dudosas y atribuciones sin confirmar.
6. Comprueba texto, tiempos, voces y avisos locales. Entrega las rutas de los resultados e indica las limitaciones y la revisión pendiente. No inventes acuerdos ni tareas; no envíes ni publiques nada y no modifiques Git sin autorización específica.
