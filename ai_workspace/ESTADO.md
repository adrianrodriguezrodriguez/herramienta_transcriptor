# Estado — 30/10/2026

Versión 1 operativa. Bloques 0 y 1 hechos; bloque 2 verificado salvo limpieza del origen.
PLAN_ACTUAL.md se conserva intacto por instrucción expresa; su estado BORRADOR no refleja la ejecución.

## Hecho

- Entorno Python 3.11, CUDA y large-v3 local; dependencias fijadas y README de instalación/uso.
- Consola local: conversión temporal, transcripción y repaso, voces, nombres con evidencia,
  cuatro salidas y avisos de revisión. Sin subidas ni modificación de originales.
- Recuperación de memoria al cargar, consumir segmentos o repasar: medium local y después
  el modelo solicitado en CPU; reinicio sin duplicar resultados. Otros errores se propagan.
- OCR de rótulos sintéticos verificado; abstención ante solapes, contradicciones o nombres
  compartidos por voces. Un tiempo de espera agotado del OCR no impide terminar.
- Resemblyzer 0.1.4 empaquetado con webrtcvad-wheels; no fue necesario cambiar de motor.

## Verificación

- Suite completa: 22 correctas, 1 omitida (tiny no descargado). Red bloqueada en pytest.
- Un aviso de obsolescencia de SciPy dentro de Resemblyzer, sin fallos.
- pip check correcto; ayuda de consola correcta. Graphify actualizado localmente.
- Salida previa dos_timbres_20261030_112803_161929 conservada: large-v3 CUDA int8_float16,
  dos voces y cuatro archivos. No se repitió esa ejecución.
- Las pruebas sintéticas comprueban el funcionamiento, no la exactitud sobre habla real.
  El ASR produjo texto sobre timbres sin palabras, señalado en revisar.md; revisar siempre.
- Fallos de memoria simulados; no se forzó un agotamiento real de VRAM.

## Pendiente y siguiente paso

- Usuario: probar una grabación propia y revisar texto, voces y nombres.
- Origen C:\Users\iovip\.codex\tmp\io_066_auditoria conservado: incluye datos y documentación
  adicionales cuya prescindibilidad no está comprobada. No se envió nada a la Papelera ni
  se liberó espacio en esta continuación. Revisarlo antes de desecharlo.
- Commit local de entrega: Transcriptor 1.0, Adrian Rodriguez, sin firmas de IA ni push.
  Sin acciones pendientes de mensajes o publicación.
