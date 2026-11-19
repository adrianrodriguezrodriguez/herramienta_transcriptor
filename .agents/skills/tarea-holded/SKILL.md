---
name: tarea-holded
description: Líneas del día para Holded. Revisa todos los proyectos de C:\Proyectos tocados en la fecha pedida (hoy por defecto) y da, por tarea, código, categoría y una línea lista para pegar.
---

1. Fecha: la del argumento (`ayer`, `10/11`, `10/11/2026`) o hoy. Solo lectura: no cambies
   archivos ni Git y no recuerdes Holded en otras órdenes.
2. Busca en `C:\Proyectos`, hasta tres niveles, las carpetas con `.git` o `ai_workspace/`. En cada
   una, de ese día: `git log --all` con la fecha y la identidad del usuario, filas de
   `ai_workspace/registro_trabajo.md`, `ESTADO.md`, `progreso.md` y archivos cambiados en
   `ai_workspace/` y `docs/`. Ignora lo automático: `graphify-out/`, `node_modules/`, `bin/`,
   `obj/`, cachés y temporales.
3. Junta las carpetas del mismo proyecto (el mismo código, p. ej. IO066, en la copia de trabajo y en
   su clon de Git). Descarta las que solo tengan cambios automáticos.
4. Tarea y categoría: usa el código y el nombre exactos si el usuario adjunta su lista de Holded o
   si constan en el proyecto o en la memoria. Si no, propón la más probable y añade «(confirmar)».
   Si en un proyecto hubo trabajo de dos tareas, da una línea por tarea. Categorías: Diseño,
   Marketing, Desarrollo, Gestión de proyectos, Desarrollo comercial, Producción, Administración,
   Integración y puesta en marcha, Soporte técnico.
5. Cada línea: una sola frase de 200 a 300 caracteres con lo hecho, en palabras de planta y
   separado por comas. Nunca nombres la IA ni la ayuda recibida (Claude, Codex, ChatGPT, «con
   ayuda de»). Sin claves, direcciones, correos, horas ni códigos internos sin explicar.
6. Responde solo con la lista: `**CÓDIGO Tarea · Categoría**` y debajo la línea en un bloque de
   código para copiarla. Al final, en una línea, los proyectos revisados sin trabajo ese día.
