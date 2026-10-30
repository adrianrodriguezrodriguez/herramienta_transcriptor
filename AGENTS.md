# Transcriptor local de reuniones

Vídeo o audio a texto con tiempos y hablantes; nombres solo con evidencia; todo local.

Autoría: Adrián Rodríguez Rodríguez. Ninguna IA figura como autora ni firma nada.

## Forma de trabajar

- Responde en español, breve y directo. Da un aviso breve al empezar cada fase (investigar, cambiar, verificar).
- Antes de una tarea mediana o grande, indica en una línea el modelo en uso y el esfuerzo que recomiendas.
- No expongas el enfoque salvo al planificar. Si una duda cambia el resultado, pregunta (cinco como
  máximo, juntas) y espera; después trabaja sin paradas salvo un bloqueo real. Sin dudas, actúa.
- El chat prevalece sobre estos documentos. Si el usuario decide algo nuevo o cambia algo escrito,
  actualiza el documento afectado en el mismo trabajo, sin esperar a que lo pida.
- Comprueba rutas y datos reales antes de usarlos; no inventes. Di lo que no hayas podido comprobar.
- Git: lee sin pedir permiso (`status`, `diff`, `log`, `show`, `blame`, `branch --list`, `remote -v`). Antes de cualquier operación que cambie algo (`add`, `commit`, `push`, `pull`, `fetch`, `checkout`, `switch`, `restore`, `reset`, `stash`, `merge`, `rebase`, `tag`, crear o borrar ramas, `config`, `init`, `clone`, `clean` o publicación), di exactamente qué vas a hacer, pide permiso y espera. El permiso vale solo para esa operación.
- Al terminar: qué se hizo, cómo se verificó y qué queda. Sin volcados de consola.

## Proyecto

- Plataformas: Windows 11.
- Tecnologías: Python 3.11; faster-whisper; ctranslate2; torch CUDA 12.4; resemblyzer; webrtcvad; scikit-learn; ffmpeg.
- Vídeo y audio se procesan en local; nunca se suben.
- Nombres de hablantes solo con evidencia; sin reconocimiento facial.
- Las grabaciones del usuario no se modifican ni se copian al repositorio.
- Intocable sin orden expresa: entrada/ (originales del usuario).

## Verificación

Proporcional al riesgo: en cambios pequeños, solo lo afectado; todo en cambios grandes y al cerrar.

- `.venv\Scripts\python -m pytest`

## Estado, planes y memoria

- Estado: `ai_workspace/ESTADO.md`. Si existe `PLAN_ACTUAL.md`, léelo antes de retomar.
- Skills: `crear-plan` planifica y para; `ejecutar-plan` ejecuta (la orden aprueba el plan);
  `cerrar` verifica, compacta y archiva, o deja el traspaso si solo se pausa; `error` diagnostica;
  `progreso` (= `estado`) retoma y da el avance (`ai_workspace/progreso.md`). Mensajes: según
  `ai_workspace/contexto/personas.md`; nada está enviado sin confirmarlo el usuario.
- `ai_workspace/` guarda solo documentos breves y vigentes: ni copias de código, ni binarios, ni
  informes viejos, ni traspasos duplicados. Los temporales van fuera del proyecto. Los límites de
  tamaño están en `ai_workspace/configuracion.json`.
- Graphify: antes de abrir archivos grandes, `graphify explain <símbolo>` o `graphify affected <símbolo>`. `cerrar` lo actualiza.

## Documentación bajo demanda

Rutas dentro de `ai_workspace/`.

| Si vas a… | Lee |
|---|---|
| cambiar la estructura del código | `contexto/arquitectura.md` |

PLAN_ACTUAL.md se conserva intacto. En esta ejecución están autorizados Git local y commits, sin remoto ni push. No usar grabaciones reales en pruebas.
