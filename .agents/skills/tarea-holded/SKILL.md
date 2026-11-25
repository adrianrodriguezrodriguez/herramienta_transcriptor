---
name: tarea-holded
description: Líneas del día para Holded. Revisa todos los proyectos de C:\Proyectos tocados en la fecha pedida (hoy por defecto) y da, por tarea de Holded, proyecto, tarea, categoría, horas y una línea lista para pegar.
---

1. Fecha: la del argumento (`ayer`, `10/11`, `10/11/2026`) o hoy. Solo lectura: no cambies
   archivos ni Git y no recuerdes Holded en otras órdenes.
2. Lee la lista de tareas del usuario en `C:\Proyectos\holded_tareas.md`. Si no existe o el usuario
   adjunta una captura más reciente, usa la captura y propón actualizar el archivo.
3. Busca en `C:\Proyectos`, hasta tres niveles, las carpetas con `.git` o `ai_workspace/`. En cada
   una, de ese día: `git log --all` con la fecha y la identidad del usuario, filas de
   `ai_workspace/registro_trabajo.md`, `ESTADO.md`, `progreso.md` y archivos cambiados en
   `ai_workspace/` y `docs/`. Ignora lo automático: `graphify-out/`, `node_modules/`, `bin/`,
   `obj/`, cachés y temporales.
4. Asigna cada trabajo a una tarea de la lista (código y nombre exactos). Una línea por tarea de
   Holded, no por tema: si todo cae en la misma tarea, una sola línea. Lo de herramientas internas,
   plantillas y organización va a la tarea de investigación/organización de la lista. Solo si nada
   encaja, propón una y añade «(confirmar)».
5. Categoría, solo una de estas: Diseño, Marketing, Desarrollo, Gestión de proyectos, Desarrollo
   comercial, Producción, Administración.
6. Horas: el día suma 8 h, repartidas según lo trabajado en cada tarea, en múltiplos de 0,5. Más
   de 8 solo si el usuario dice que hizo horas extra.
7. Cada línea: una sola frase de 200 a 300 caracteres con lo hecho, en palabras de planta y
   separado por comas. Nunca nombres la IA ni la ayuda recibida (Claude, Codex, ChatGPT, «con
   ayuda de»). Sin claves, direcciones, correos, horas ni códigos internos sin explicar.
8. Responde solo con la lista. Por tarea: `**Proyecto X · Tarea CÓDIGO Nombre · Categoría · N h**`
   y debajo la línea en un bloque de código para copiarla. Al final: el total de horas y, en una
   línea, los proyectos revisados sin trabajo ese día.
