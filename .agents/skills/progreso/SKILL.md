---
name: progreso
description: Retomar y ver el avance de todo el proyecto con formato fijo: lo pedido, fases con %, en marcha, esperas, mensajes y qué hace ahora cada uno, con textos listos. Mantiene ai_workspace/progreso.md con solo lo nuevo.
---

1. Lee `ai_workspace/progreso.md` y, si existe, `PLAN_ACTUAL.md`. Lo nuevo: archivos de
   `ai_workspace/` y `docs/` modificados tras su «Actualizado», el chat y, con Git, `status` y
   `log -5 --oneline`. Si está vacío, rellénalo una vez con `ESTADO.md`, plan, calendario y registro.
2. Comprueba lo que está en marcha (procesos, carpetas, latidos: ¿vivo?, ¿fin?) y `## Verificación`
   de `AGENTS.md`. Si otra IA o una prueba usa el proyecto, compila en una carpeta temporal o no
   compiles y dilo.
3. Actualiza `progreso.md` con sus secciones (6 KB máx.; sustituye, no acumules; en «Lo pedido»,
   hoy y lo abierto). Relee antes de guardar: si otra IA lo cambió, mezcla. Pon al día la línea de
   `ESTADO.md` y las casillas del calendario o del plan, si existen, con fecha. Nunca código,
   configuración ni Git.
4. Responde siempre con esas secciones y en ese orden, igual en Claude y Codex, tras
   `## Progreso — dd/mm hh:mm` y una línea de resumen. ✅ comprobado, 🟡 sin comprobar,
   ⏳ en curso, — sin empezar. % = tareas hechas / totales del calendario o plan (o «estimado»).
   ¿Insistir? solo si pasó una fecha pactada o bloquea, y a través de quién.
5. Si hace falta, termina con textos completos: prompt (leer `AGENTS.md` y el estado, qué hacer,
   qué no tocar, qué informar) y mensajes según `ai_workspace/contexto/personas.md`, anotados
   como «preparado» hasta que el usuario confirme el envío.
6. Distingue lo comprobado de lo declarado; no inventes avances.
