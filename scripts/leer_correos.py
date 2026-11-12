"""Lector de correos de licitaciones y generador de borradores de consultas (Habilidades 01, 16, 17).

Modos de uso:
1) Procesar un archivo .eml local (y crear o actualizar la licitación):
   python scripts/leer_correos.py --eml ruta/al/correo.eml [--codigo LIC-2026-001]

2) Consultar bandeja Gmail vía IMAP (solo lectura; lee credenciales desde variables de entorno o Token Vault):
   python scripts/leer_correos.py --imap --dias 7

3) Generar un borrador .eml de consultas al mandante (NUNCA envía correos por sí solo; queda listo para revisión de Carlos):
   python scripts/leer_correos.py --borrador-consultas <CODIGO> --ronda 1
"""
from __future__ import annotations

import argparse
import email
import imaplib
import json
import os
import re
from datetime import datetime, timedelta
from email import policy
from email.message import EmailMessage
from pathlib import Path

from nueva_licitacion import crear_licitacion

ROOT = Path(__file__).resolve().parent.parent
LIC_DIR = ROOT / "licitaciones"

PALABRAS_CLAVE_CLASIFICACION = {
    "ADENDA": ["adenda", "modificación de bases", "rectificación", "enmienda", "prórroga"],
    "RESPUESTAS": ["serie de respuestas", "aclaraciones", "respuestas a las consultas", "foro de preguntas"],
    "ADJUDICACION": ["adjudicación", "resultado de la licitación", "acta de evaluación"],
    "INVITACION": ["invitación a licitar", "bases de licitación", "llamado a licitación", "solicitud de propuesta", "rfp", "rfq", "cotización"],
}


def clasificar_correo(asunto: str, cuerpo: str) -> str:
    texto = f"{asunto} {cuerpo}".lower()
    for tipo, palabras in PALABRAS_CLAVE_CLASIFICACION.items():
        if any(p in texto for p in palabras):
            return tipo
    return "INVITACION"


def extraer_metadatos_licitacion(asunto: str, cuerpo: str, remitente: str) -> dict[str, str]:
    texto = f"{asunto}\n{cuerpo}"
    # Buscar código tipo LIC-2026-XXX, ID Mercado Público (1234-56-LP26 / LE26 / LQ26), RFP-XXX, etc.
    patrones_codigo = [
        r"\b(\d{3,6}-\d{1,4}-L[PEQRO]\d{2})\b",
        r"\b(LIC-\d{4}-\d{2,4})\b",
        r"\b(RFP-\d{4}-\d{2,4})\b",
        r"\b(SP-\d{4,8})\b",
    ]
    codigo = None
    for pat in patrones_codigo:
        m = re.search(pat, texto, re.IGNORECASE)
        if m:
            codigo = m.group(1).upper()
            break
    if not codigo:
        codigo = f"LIC-{datetime.now().strftime('%Y%m%d-%H%M')}"

    # Buscar fecha de cierre (YYYY-MM-DD o DD/MM/YYYY o DD-MM-YYYY)
    cierre = None
    m_iso = re.search(r"cierre[^\n\d]{0,30}(\d{4}-\d{2}-\d{2}(?:\s+\d{2}:\d{2})?)", texto, re.IGNORECASE)
    if m_iso:
        cierre = m_iso.group(1)
    else:
        m_cl = re.search(r"cierre[^\n\d]{0,30}(\d{2})[/-](\d{2})[/-](\d{4})(?:\s+a\s+las\s+(\d{2}:\d{2}))?", texto, re.IGNORECASE)
        if m_cl:
            d, mes, y, h = m_cl.groups()
            cierre = f"{y}-{mes}-{d} {h or '15:00'}"

    # Mandante desde dominio o línea "Mandante:"
    m_mand = re.search(r"(?:mandante|cliente|empresa)\s*:\s*([^\n\r]+)", texto, re.IGNORECASE)
    if m_mand:
        mandante = m_mand.group(1).strip()
    else:
        m_dom = re.search(r"@([\w.-]+)", remitente or "")
        mandante = m_dom.group(1) if m_dom else "Mandante por confirmar"

    portal = "Mercado Público" if "mercadopublico" in texto.lower() else (
        "SAP Ariba" if "ariba" in texto.lower() else "Correo directo / Portal Mandante"
    )
    nombre = re.sub(r"^(re|rv|fwd|fw)\s*:\s*", "", asunto.strip(), flags=re.IGNORECASE)
    return {
        "codigo": codigo,
        "nombre": nombre or f"Licitación {codigo}",
        "mandante": mandante,
        "portal": portal,
        "cierre": cierre,
    }


def procesar_mensaje_email(msg: email.message.EmailMessage, codigo_forzado: str | None = None) -> Path:
    asunto = str(msg.get("Subject", "Sin asunto"))
    remitente = str(msg.get("From", ""))
    fecha = str(msg.get("Date", datetime.now().isoformat()))

    cuerpo = ""
    if msg.is_multipart():
        for part in msg.walk():
            ctype = part.get_content_type()
            if ctype == "text/plain" and not part.get_filename():
                cuerpo += part.get_content()
    else:
        cuerpo = msg.get_content()

    tipo = clasificar_correo(asunto, cuerpo)
    meta = extraer_metadatos_licitacion(asunto, cuerpo, remitente)
    codigo = codigo_forzado or meta["codigo"]

    dest = crear_licitacion(
        codigo=codigo,
        nombre=meta["nombre"],
        mandante=meta["mandante"],
        portal=meta["portal"],
        cierre=meta["cierre"],
    )

    # Guardar copia del .eml y resumen en correo/
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    eml_out = dest / "correo" / f"{ts}_{tipo.lower()}.eml"
    eml_out.write_bytes(msg.as_bytes())

    adjuntos_guardados: list[str] = []
    for part in msg.walk():
        fname = part.get_filename()
        if fname:
            safe_name = re.sub(r"[^\w.\- ()]", "_", fname)
            out_file = dest / "bases" / safe_name
            out_file.write_bytes(part.get_payload(decode=True))
            adjuntos_guardados.append(safe_name)

    resumen_md = (
        f"# Registro de Correo Recibido — `{codigo}`\n\n"
        f"- **Clasificación automática:** `{tipo}`\n"
        f"- **Asunto:** {asunto}\n"
        f"- **De:** {remitente}\n"
        f"- **Fecha:** {fecha}\n"
        f"- **Portal detectado:** {meta['portal']}\n"
        f"- **Cierre detectado:** {meta['cierre'] or 'Revisar en bases'}\n"
        f"- **Adjuntos descargados a `bases/`:** {', '.join(adjuntos_guardados) if adjuntos_guardados else 'Ninguno'}\n\n"
        f"## Cuerpo del Mensaje\n\n```text\n{cuerpo.strip()}\n```\n"
    )
    (dest / "correo" / f"{ts}_{tipo.lower()}.md").write_text(resumen_md, encoding="utf-8")

    # Registrar en estado.json
    estado_path = dest / "estado.json"
    estado = json.loads(estado_path.read_text(encoding="utf-8"))
    estado["historial"].append(
        {
            "fecha_hora": datetime.now().isoformat(timespec="seconds"),
            "evento": f"Correo procesado ({tipo}): {asunto} | Adjuntos: {len(adjuntos_guardados)}",
        }
    )
    estado_path.write_text(json.dumps(estado, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"[OK] Correo ({tipo}) procesado en {dest} | Adjuntos guardados: {len(adjuntos_guardados)}")
    return dest


def generar_borrador_consultas(codigo: str, ronda: int = 1) -> Path:
    dest = LIC_DIR / codigo
    ficha = json.loads((dest / "ficha.json").read_text(encoding="utf-8"))
    preguntas_md_path = dest / "consultas" / f"preguntas_ronda_{ronda}.md"
    if not preguntas_md_path.exists():
        preguntas_md_path.write_text(
            f"# Consultas al Mandante — Ronda {ronda} (`{codigo}`)\n\n"
            "| N° | Documento | Numeral / Página | Cita de las Bases | Consulta Formulada |\n"
            "|---:|---|---|---|---|\n"
            "| 1 | TdR | Numeral 4.2, pág. 9 | Acceso a plataformas y permisos | Favor confirmar que los permisos de acceso superficial y servidumbres serán gestionados íntegramente por el Mandante antes de la movilización a terreno. |\n"
            "| 2 | BAG | Numeral 8.2, pág. 14 | Garantía de seriedad de la oferta | Favor confirmar si se acepta Póliza de Seguro de Garantía a Primer Requerimiento como alternativa a la Boleta Bancaria. |\n"
            "| 3 | BAE | Numeral 6.1, pág. 11 | Plazo de ejecución | Favor confirmar si los días de revisión del Informe Borrador (Rev. B) por parte del Mandante se contabilizan fuera del plazo contractual de ejecución del Consultor. |\n",
            encoding="utf-8",
        )

    cuerpo_preguntas = preguntas_md_path.read_text(encoding="utf-8")
    msg = EmailMessage()
    msg["Subject"] = f"Consultas Licitación {codigo} — {ficha.get('nombre', '')} — Geologgia Ltda."
    msg["From"] = "licitaciones@geologgia.cl"
    msg["To"] = ficha.get("contacto_oficial", {}).get("email", "contacto@mandante.cl")
    msg["X-Unsent"] = "1"  # Permite abrirlo en Outlook/Thunderbird listo para editar y enviar manualmente
    msg.set_content(
        f"Estimados señores {ficha.get('mandante', '')},\n\n"
        f"Junto con saludar, en el marco del proceso de licitación '{ficha.get('nombre', '')}' ({codigo}), "
        f"enviamos a continuación nuestras consultas de la Ronda {ronda} para vuestra gentil aclaración:\n\n"
        f"{cuerpo_preguntas}\n\n"
        f"Atentamente,\n"
        f"Carlos Cristian Ávila Elgueta\n"
        f"Socio Director — Geologgia Ltda.\n"
        f"www.geologgia.cl\n"
    )
    out_eml = dest / "consultas" / f"BORRADOR_consultas_ronda_{ronda}.eml"
    out_eml.write_bytes(msg.as_bytes())
    print(f"[OK] Borrador de consultas (NO enviado; requiere revisión humana) creado en: {out_eml}")
    return out_eml


def leer_imap_gmail(dias: int = 7) -> None:
    user = os.environ.get("GMAIL_USER")
    app_pw = os.environ.get("GMAIL_APP_PASSWORD")
    if not user or not app_pw:
        print(
            "[INFO] Para lectura directa de Gmail por IMAP defina GMAIL_USER y GMAIL_APP_PASSWORD en su entorno o Token Vault.\n"
            "       También puede usar `--eml archivo.eml` con cualquier correo descargado."
        )
        return
    since_str = (datetime.now() - timedelta(days=dias)).strftime("%d-%b-%Y")
    with imaplib.IMAP4_SSL("imap.gmail.com") as M:
        M.login(user, app_pw)
        M.select("INBOX", readonly=True)
        typ, data = M.search(None, f'(SINCE "{since_str}")')
        if typ != "OK":
            return
        for num in data[0].split():
            typ, msg_data = M.fetch(num, "(RFC822)")
            if typ == "OK" and msg_data and msg_data[0]:
                raw = msg_data[0][1]
                msg = email.message_from_bytes(raw, policy=policy.default)
                subj = str(msg.get("Subject", "")).lower()
                if any(k in subj for k in ["licitac", "propuesta", "rfp", "bases", "adenda", "cotizac", "mercadopublico"]):
                    procesar_mensaje_email(msg)


def main() -> None:
    parser = argparse.ArgumentParser(description="Procesa correos de licitación o genera borradores de consulta.")
    parser.add_argument("--eml", help="Ruta a un archivo .eml local para procesar")
    parser.add_argument("--codigo", default=None, help="Código de licitación al cual asociar el correo")
    parser.add_argument("--imap", action="store_true", help="Buscar correos recientes en Gmail (IMAP solo lectura)")
    parser.add_argument("--dias", type=int, default=7, help="Días hacia atrás para buscar en IMAP")
    parser.add_argument("--borrador-consultas", dest="borrador_codigo", help="Genera borrador .eml de consultas para <CODIGO>")
    parser.add_argument("--ronda", type=int, default=1, help="Número de ronda de consultas")
    args = parser.parse_args()

    if args.eml:
        raw = Path(args.eml).read_bytes()
        msg = email.message_from_bytes(raw, policy=policy.default)
        procesar_mensaje_email(msg, codigo_forzado=args.codigo)
    elif args.borrador_codigo:
        generar_borrador_consultas(args.borrador_codigo, args.ronda)
    elif args.imap:
        leer_imap_gmail(args.dias)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
