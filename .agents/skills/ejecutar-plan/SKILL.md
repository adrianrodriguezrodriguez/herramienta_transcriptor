---
name: ejecutar-plan
description: Ejecuta PLAN_ACTUAL.md cuando el usuario ordena empezar o continuar un plan.
---

La orden del usuario aprueba el plan.

1. Lee `PLAN_ACTUAL.md`. Si está `COMPLETADO`, `INCOMPLETO` o `BLOQUEADO`, avisa y para.
2. Pasa el estado a `EN CURSO`:
   `powershell -NoProfile -File ai_workspace/tools/planes.ps1 -Accion Estado -Estado "EN CURSO"`
3. Ejecuta los bloques en orden, sin rediseñar ni añadir extras. Para solo ante una contradicción,
   una decisión que falte o un riesgo real.
4. Marca cada bloque `[HECHO]` en una línea y deja escrito el siguiente paso; no narres el trabajo
   dentro del plan.
5. Verifica en proporción al riesgo durante el trabajo y con todos los comandos de `AGENTS.md` al
   final.
6. Todo hecho y verificado: estado `COMPLETADO`. Si no puedes seguir: `BLOQUEADO`, con el motivo en
   el plan. No lo archives; eso lo hace `cerrar`.
