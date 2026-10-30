from pathlib import Path
import json
from .asr import dudas


def tiempo(segundos, milisegundos=False):
    total = max(0, round(segundos * 1000))
    horas, resto = divmod(total, 3600000)
    minutos, resto = divmod(resto, 60000)
    segundos, ms = divmod(resto, 1000)
    return f"{horas:02d}:{minutos:02d}:{segundos:02d}" + (f",{ms:03d}" if milisegundos else "")


def escribir(destino: Path, segmentos, meta, nombres, diarizacion, evidencias):
    destino.mkdir(parents=True, exist_ok=False)
    cabecera = ["# Transcripción local", "", f"- Duración: {tiempo(meta['duration'])}",
                f"- Modelo: {meta['model']} ({meta['device']}, {meta['compute_type']})",
                f"- Idioma: {meta['language']}", f"- Hablantes detectados: {len(nombres)}", "",
                "## Procedencia de los nombres", ""]
    cabecera += [f"- {voz}: {dato['name']} — {dato['source']}" for voz, dato in nombres.items()]
    cabecera += ["", "## Texto", ""]
    subtitulos, revision = [], ["# Revisar", "", "La diarización es aproximada. Revisar nombres y posibles mezclas de voces.", ""]
    for voz, dato in nombres.items():
        if dato["name"] != voz:
            revision.append(f"- Revisar {voz} → {dato['name']}: {dato['source']}.")
    for i, segmento in enumerate(segmentos, 1):
        nombre = nombres.get(segmento["speaker"], {}).get("name", segmento["speaker"])
        cabecera.append(f"[{tiempo(segmento['start'])}] {nombre}: {segmento['text']}")
        subtitulos.append(f"{i}\n{tiempo(segmento['start'], True)} --> {tiempo(segmento['end'], True)}\n{nombre}: {segmento['text']}\n")
        motivos = dudas(segmento)
        if segmento.get("possible_overlap"):
            motivos.append("posible solape o cambio de hablante dentro del tramo")
        if segmento["speaker"] == "Hablante sin determinar":
            motivos.append("sin voz asignable")
        if motivos:
            revision.append(f"- [{tiempo(segmento['start'])}–{tiempo(segmento['end'])}] {', '.join(motivos)}: {segmento['text']}")
    revision.extend(f"- Aviso: {a}" for a in meta.get("warnings", []))
    datos = {"metadata": meta, "speakers": nombres, "segments": segmentos,
             "diarization": diarizacion, "visual_evidence": evidencias}
    for nombre, texto in (("transcripcion.md", "\n".join(cabecera)),
                          ("transcripcion.srt", "\n".join(subtitulos)),
                          ("revisar.md", "\n".join(revision)),
                          ("transcripcion.json", json.dumps(datos, ensure_ascii=False, indent=2))):
        (destino / nombre).write_text(texto + "\n", encoding="utf-8")
