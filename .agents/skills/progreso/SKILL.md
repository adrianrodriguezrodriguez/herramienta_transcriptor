---
name: progreso
description: Retomar o recuperar el hilo. Da al grano qué llevamos y qué falta, qué hay que recordar, mandar o revisar, y qué hace ahora cada uno: Codex (encargo listo para copiar), Claude (¿hago esto?) y el usuario (lo mínimo, casi siempre revisar).
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
4. Responde igual en Claude y Codex, al grano pero con los detalles importantes, sin relleno:
   - `## Progreso — dd/mm hh:mm` y debajo **Dónde estábamos:** (lo último hecho) · **Siguiente:**.
   - `### Lo que llevamos y lo que falta`: tabla de fases (estado, %, qué falta) y tabla de
     peticiones abiertas. ✅ comprobado, 🟡 sin comprobar, ⏳ en curso, — sin empezar.
     % = tareas hechas / totales del plan o calendario (o «estimado»), uno por fase.
   - `### Recordar, mandar o revisar`: tabla (quién, qué, desde cuándo, a través de quién).
     Solo lo que el usuario tiene que recordar, enviar o revisar.
   - `### Ahora`, en tres bloques y en este orden:
     **Codex** → el encargo completo en un bloque de código plano (leer `AGENTS.md` y el estado,
     qué hacer, qué no tocar, sin Git salvo autorización, avisar con `FIN` al acabar), o «nada».
     **Claude** → preguntas numeradas «¿Hago …?» (sí/no). Si Codex terminó algo, la primera es
     «¿Reviso lo que hizo Codex?».
     **Tú** → lo mínimo, casi siempre revisar: qué mirar y dónde (ruta absoluta en bloque de código).
   - `### Bloqueado por otros`: lista corta; ¿insistir? solo si pasó una fecha pactada o bloquea.
   Títulos y subtítulos siempre marcados. Lo pendiente sale en el mismo orden que la vez anterior.
   Lo ya enviado no se nombra salvo que el usuario pregunte.
5. Mensajes para otras personas (según `ai_workspace/contexto/personas.md`): completos y en un
   bloque de código plano, sin firma, anotados como «preparado» hasta que el usuario confirme el envío.
6. Distingue lo comprobado de lo declarado («según X»); no inventes avances.
