---
name: crear-plan
description: Crea PLAN_ACTUAL.md cuando el usuario pide un plan para ejecutarlo después. Nunca lo ejecuta.
---

1. Si ya existe `PLAN_ACTUAL.md`, no preguntes qué hacer con él: archívalo tal cual con
   `ai_workspace/tools/planes.ps1 -Accion Archivar` (`COMPLETADO` si todo estaba hecho; si no,
   `INCOMPLETO`) y lleva al plan nuevo sus decisiones vigentes y lo pendiente que siga valiendo,
   sin las tareas hechas. Lo que ya no valga, dilo al entregar.
2. Investiga lo justo: Graphify si está activo y después solo los fragmentos necesarios.
3. Haz juntas todas las preguntas que cambien el alcance, los datos, la aceptación o las plataformas.
4. Escribe `PLAN_ACTUAL.md` dentro de su límite de tamaño (`ai_workspace/configuracion.json`):
   título, `> **Estado:** BORRADOR`, objetivo, decisiones, intocables, archivos y símbolos, bloques
   numerados `[ ]`, pruebas y criterios de aceptación, riesgos y cómo volver atrás. Lo justo para
   que otra IA lo ejecute sin repetir la investigación; sin copiar documentación existente.
5. Di dónde quedó y para. No ejecutes nada.
