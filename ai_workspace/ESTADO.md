# Estado — 30/10/2026

Versión 1 terminada y publicada en GitHub (`origin/main`). Plan de arranque y versión 1 archivado como COMPLETADO.

## Hecho

- Entorno Python 3.11, CUDA y large-v3 local; dependencias fijadas y README de instalación/uso.
- Consola local: conversión temporal, transcripción y repaso, voces, nombres con evidencia,
  cuatro salidas y avisos de revisión. Sin subidas ni modificación de originales.
- Recuperación de memoria al cargar, consumir segmentos o repasar: medium local y después
  el modelo solicitado en CPU; reinicio sin duplicar resultados. Otros errores se propagan.
- OCR de rótulos sintéticos verificado; abstención ante solapes, contradicciones o nombres
  compartidos por voces. Un tiempo de espera agotado del OCR no impide terminar.
- Resemblyzer 0.1.4 empaquetado con webrtcvad-wheels; no fue necesario cambiar de motor.
- Repositorio publicado: https://github.com/adrianrodriguezrodriguez/herramienta_transcriptor (rama `main`).
- Origen `C:\Users\iovip\.codex\tmp\io_066_auditoria` retirado por orden del usuario: venv antiguo
  y audios de la reunión del 29/10 borrados definitivamente; scripts y JSON a la Papelera. ~5 GB liberados.
- Salida sintética `dos_timbres_…` enviada a la Papelera.

## Verificación

- Suite completa: 22 correctas, 1 omitida (tiny no descargado). Red bloqueada en pytest.
- Un aviso de obsolescencia de SciPy dentro de Resemblyzer, sin fallos.
- pip check correcto; ayuda de consola correcta. Graphify actualizado localmente.
- Ejecución sintética con large-v3 CUDA int8_float16: dos voces y cuatro archivos.
- Las pruebas sintéticas comprueban el funcionamiento, no la exactitud sobre habla real.
- Fallos de memoria simulados; no se forzó un agotamiento real de VRAM.
- Push comprobado: `main...origin/main` sin diferencias. Origen comprobado inexistente.

## Pendiente y siguiente paso

- Usuario: probar una grabación propia en `entrada/` y revisar texto, voces y nombres.
- Mejora opcional futura: pyannote (requiere token de Hugging Face y licencias).
