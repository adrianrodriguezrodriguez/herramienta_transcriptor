---
name: progreso
description: Retomar o recuperar el hilo. Da al grano qué tiene que hacer el usuario y en qué orden, qué llevamos y qué falta, qué mandar o revisar, y qué hace cada uno: Codex (encargo listo para copiar), Claude (¿hago esto?) y el usuario.
---

1. Repaso rápido: si `ai_workspace/progreso.md` se actualizó hace menos de 30 minutos y desde
   entonces no han cambiado archivos de `ai_workspace/`, `docs/` ni Git, no vuelvas a revisar:
   repite la respuesta del paso 4 en corto, con «Sin cambios desde hh:mm».
2. Si no, lee `progreso.md` y `PLAN_ACTUAL.md` (si existe), los archivos de `ai_workspace/` y
   `docs/` modificados tras su «Actualizado», el chat y, con Git, `status` y `log -5 --oneline`.
   Mira si hay algo en marcha (procesos, carpetas, latidos: ¿vivo?, ¿terminó?). No compiles ni
   pases pruebas. Si `progreso.md` está vacío, rellénalo una vez con `ESTADO.md`, plan y registro.
3. Actualiza `progreso.md` con sus secciones (6 KB máx.; sustituye, no acumules). Relee antes de
   guardar: si otra IA lo cambió, mezcla. Pon al día la línea de `ESTADO.md` y las casillas del
   calendario o del plan, si existen, con fecha. Nunca código, configuración ni Git.
4. Responde igual en Claude y Codex, corto y sin tablas (listas), en este orden:
   - `## Progreso — dd/mm hh:mm` y debajo **Dónde estábamos:** (lo último hecho, una o dos frases)
     · **Siguiente:**.
   - `### Lo que haces tú, en orden`: pasos numerados y completos (dónde, qué verá, qué hacer si
     sale A o B). Los mensajes para otras personas van dentro de su paso, completos y en bloque de
     código; las rutas, absolutas y en bloque de código. Si no tiene nada que hacer, dilo.
   - `### Lo que llevamos y lo que falta`: una línea por fase con ✅ comprobado, 🟡 sin
     comprobar, ⏳ en curso o — sin empezar, el % (hechas / totales del plan o calendario, o
     «estimado») y qué falta. Después, las peticiones abiertas, una por línea.
   - `### Qué hacemos Codex y yo`: **Codex** → el encargo completo en un bloque de código plano
     (leer `AGENTS.md` y el estado, qué hacer, qué no tocar, sin Git salvo autorización, avisar con
     `FIN` al acabar), o «nada». **Claude** → preguntas numeradas «¿Hago …?» (sí/no); si Codex
     terminó algo, la primera es «¿Reviso lo que hizo Codex?».
   - `### Bloqueado por otros`: lista corta; ¿insistir? solo si pasó una fecha pactada o bloquea.
   Títulos siempre marcados. Lo pendiente sale en el mismo orden que la vez anterior. Lo ya enviado
   no se nombra salvo que el usuario pregunte.
5. Mensajes para otras personas (según `ai_workspace/contexto/personas.md`): completos y en un
   bloque de código plano, sin firma, anotados como «preparado» hasta que el usuario confirme el envío.
6. Distingue lo comprobado de lo declarado («según X»); no inventes avances.
