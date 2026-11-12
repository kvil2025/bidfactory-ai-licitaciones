"""Genera el Informe Ejecutivo para el Revisor Final (`revision/informe_revisor_final.docx`)
y registra la decisión formal del Aprobador en `revision/acta_aprobacion.md` y `estado.json`
(Habilidades 47 y 48).

Uso:
    # 1) Generar informe para revisión de Carlos Ávila (Habilidad 47):
    python scripts/informe_aprobacion.py <CODIGO>

    # 2) Registrar aprobación formal y precio definitivo de envío (Habilidad 48):
    python scripts/informe_aprobacion.py <CODIGO> --aprobar --precio 565.50 --moneda UF --por "Carlos Cristian Ávila Elgueta"
"""
from __future__ import annotations

import argparse
import json
from datetime import datetime
from pathlib import Path

import docx
import openpyxl
from armar_propuesta import agregar_tabla_estilizada, configurar_estilos
from docx.shared import Pt, RGBColor

ROOT = Path(__file__).resolve().parent.parent
LIC_DIR = ROOT / "licitaciones"


def leer_escenarios_costos(dest: Path) -> dict[str, float]:
    costos_xlsx = dest / "propuesta" / "economica" / "costos.xlsx"
    if not costos_xlsx.exists():
        return {"agresivo": 0.0, "objetivo": 0.0, "conservador": 0.0, "costo_directo": 0.0}
    wb = openpyxl.load_workbook(costos_xlsx, data_only=False)
    ws_hh = wb["HH_Profesionales"]
    ws_cd = wb["Costos_Directos"]

    total_hh = 0.0
    for r in range(4, ws_hh.max_row):
        tarifa = float(ws_hh.cell(row=r, column=3).value or 0)
        h1 = float(ws_hh.cell(row=r, column=4).value or 0)
        h2 = float(ws_hh.cell(row=r, column=5).value or 0)
        h3 = float(ws_hh.cell(row=r, column=6).value or 0)
        total_hh += tarifa * (h1 + h2 + h3)

    total_cd_no_hh = 0.0
    for r in range(4, ws_cd.max_row):
        cant = float(ws_cd.cell(row=r, column=5).value or 0)
        pu = float(ws_cd.cell(row=r, column=6).value or 0)
        total_cd_no_hh += cant * pu

    cd = total_hh + total_cd_no_hh
    gg = cd * 0.12
    c_agr = (cd + gg + cd * 0.03) * 1.12
    c_obj = (cd + gg + cd * 0.06) * 1.18
    c_con = (cd + gg + cd * 0.10) * 1.25
    return {
        "costo_directo": round(cd, 2),
        "agresivo": round(c_agr, 2),
        "objetivo": round(c_obj, 2),
        "conservador": round(c_con, 2),
    }


def generar_informe_revisor_final(codigo: str) -> Path:
    dest = LIC_DIR / codigo
    ficha = json.loads((dest / "ficha.json").read_text(encoding="utf-8"))
    estado = json.loads((dest / "estado.json").read_text(encoding="utf-8"))
    req_data = json.loads((dest / "analisis" / "requisitos.json").read_text(encoding="utf-8"))
    reqs = req_data.get("requisitos", [])
    criterios = req_data.get("criterios", [])
    precios = leer_escenarios_costos(dest)

    total_req = len(reqs)
    cumple_req = sum(1 for r in reqs if r.get("estado") == "Cumple")
    inadm_pend = [r for r in reqs if r.get("causal_inadmisibilidad") and r.get("estado") != "Cumple"]
    puntaje_sim = sum((c.get("ponderacion_pct", 0) / 100.0) * c.get("puntaje_simulado", 0) for c in criterios)

    recomendacion = "APROBAR ENVÍO" if not inadm_pend and cumple_req == total_req else "APROBAR CON CONDICIONES (CERRAR PENDIENTES CRÍTICOS)"

    doc = docx.Document()
    configurar_estilos(doc)

    p = doc.add_paragraph()
    r = p.add_run(f"INFORME EJECUTIVO PARA REVISOR FINAL Y APROBADOR (HABILIDADES 47–48)\n{codigo} — {ficha.get('nombre', '')}")
    r.bold = True
    r.font.size = Pt(15)
    r.font.color.rgb = RGBColor(0x0D, 0x25, 0x60)

    doc.add_heading("1. Ficha de Control y Recomendación de QA", level=1)
    agregar_tabla_estilizada(
        doc,
        ["Parámetro de Control", "Estado Verificado por QA"],
        [
            ["Licitación / Mandante", f"{codigo} — {ficha.get('nombre', '')} ({ficha.get('mandante', '')})"],
            ["Canal y Fecha de Cierre", f"{ficha.get('portal', '')} | {ficha.get('hitos', {}).get('cierre_ofertas', '')}"],
            ["Revisor Final y Aprobador", "Carlos Cristian Ávila Elgueta"],
            ["Cumplimiento de Requisitos", f"{cumple_req} / {total_req} ({(cumple_req/total_req*100 if total_req else 0):.1f}%)"],
            ["Causales de Inadmisibilidad Pendientes", f"{len(inadm_pend)} ({', '.join(x['id'] for x in inadm_pend) or 'Ninguna'})"],
            ["Puntaje Ponderado Simulado (Hab. 45)", f"{puntaje_sim:.2f} / 100 pts"],
            ["Recomendación al Revisor Final", recomendacion],
        ],
    )

    doc.add_heading("2. Escenarios Económicos para Decisión del Aprobador (Habilidad 34 / 48)", level=1)
    cd = precios["costo_directo"]
    agregar_tabla_estilizada(
        doc,
        ["Escenario", "Precio Neto Oferta (UF)", "Costo Directo Base (UF)", "Margen Bruto s/Venta", "Uso Recomendado"],
        [
            ["Agresivo (12% utilidad)", f"{precios['agresivo']:,.2f} UF", f"{cd:,.2f} UF", f"{((precios['agresivo']-cd)/precios['agresivo']*100 if precios['agresivo'] else 0):.1f}%", "Alta competencia por precio"],
            ["Objetivo Estándar (18% utilidad)", f"{precios['objetivo']:,.2f} UF", f"{cd:,.2f} UF", f"{((precios['objetivo']-cd)/precios['objetivo']*100 if precios['objetivo'] else 0):.1f}%", "Recomendado por equilibrio riesgo/retorno"],
            ["Conservador (25% utilidad)", f"{precios['conservador']:,.2f} UF", f"{cd:,.2f} UF", f"{((precios['conservador']-cd)/precios['conservador']*100 if precios['conservador'] else 0):.1f}%", "Alta complejidad o riesgo contractual"],
        ],
    )

    doc.add_heading("3. Detalle de Requisitos Pendientes o en Curso", level=1)
    pend_rows = [
        [r["id"], r["categoria"], r["requisito"], "SÍ" if r.get("causal_inadmisibilidad") else "NO", r["estado"], r.get("evidencia_observaciones", "")]
        for r in reqs
        if r.get("estado") != "Cumple"
    ]
    if pend_rows:
        agregar_tabla_estilizada(
            doc,
            ["ID", "Categoría", "Requisito", "Inadmisibilidad", "Estado", "Acción Requerida"],
            pend_rows,
        )
    else:
        doc.add_paragraph("Todos los requisitos de la Matriz de Cumplimiento se encuentran en estado 'Cumple'.")

    doc.add_heading("4. Resolución del Revisor Final y Aprobador", level=1)
    aprob = estado.get("aprobacion", {})
    agregar_tabla_estilizada(
        doc,
        ["Campo de Resolución", "Valor Registrado"],
        [
            ["Estado de Aprobación", aprob.get("estado", "PENDIENTE")],
            ["Aprobador", aprob.get("aprobador", "Carlos Cristian Ávila Elgueta")],
            ["Precio Final Autorizado", f"{aprob.get('precio_aprobado') or '[POR DEFINIR]'} {aprob.get('moneda', 'UF')}"],
            ["Fecha y Hora de Firma", aprob.get("fecha_hora") or "[PENDIENTE]"],
        ],
    )

    out_docx = dest / "revision" / "informe_revisor_final.docx"
    doc.save(out_docx)

    estado["revision_final"]["puntaje_tecnico_simulado"] = round(puntaje_sim, 2)
    estado["revision_final"]["observaciones_abiertas"] = len(pend_rows)
    (dest / "estado.json").write_text(json.dumps(estado, indent=2, ensure_ascii=False), encoding="utf-8")

    print(f"[OK] Informe para Revisor Final generado en: {out_docx}")
    return out_docx


def registrar_aprobacion(codigo: str, precio: float, moneda: str, por: str, observaciones: str = "") -> Path:
    dest = LIC_DIR / codigo
    estado_path = dest / "estado.json"
    estado = json.loads(estado_path.read_text(encoding="utf-8"))
    ficha = json.loads((dest / "ficha.json").read_text(encoding="utf-8"))
    ahora = datetime.now().isoformat(timespec="seconds")

    estado["estado_global"] = "APROBADA"
    estado["fase_actual"] = "VIII - Aprobación, envío y post-licitación"
    estado["habilidad_actual"] = 49
    estado["go_no_go"]["decision_aprobador"] = "GO"
    estado["go_no_go"]["aprobado_por"] = por
    estado["revision_final"]["estado"] = "VISTO BUENO OTORGADO"
    estado["aprobacion"] = {
        "estado": "APROBADA PARA ENVÍO",
        "aprobador": por,
        "precio_aprobado": precio,
        "moneda": moneda,
        "fecha_hora": ahora,
        "observaciones": observaciones,
    }
    estado["historial"].append(
        {
            "fecha_hora": ahora,
            "evento": f"Oferta APROBADA PARA ENVÍO por {por} con precio final {precio:,.2f} {moneda}",
        }
    )
    estado_path.write_text(json.dumps(estado, indent=2, ensure_ascii=False), encoding="utf-8")

    acta_md = (
        f"# Acta de Revisión Final y Aprobación de Envío (Habilidades 47–48)\n\n"
        f"- **Código de Licitación:** `{codigo}`\n"
        f"- **Nombre:** {ficha.get('nombre', '')}\n"
        f"- **Mandante:** {ficha.get('mandante', '')}\n"
        f"- **Revisor Final y Aprobador:** {por}\n"
        f"- **Decisión Formal:** **APROBADA PARA ENVÍO**\n"
        f"- **Precio Neto Autorizado:** **{precio:,.2f} {moneda}** (más impuestos según bases)\n"
        f"- **Puntaje Ponderado Simulado:** {estado['revision_final'].get('puntaje_tecnico_simulado', 'N/A')} pts\n"
        f"- **Fecha y Hora de Autorización:** `{ahora}`\n"
        f"- **Instrucciones de Despacho (Habilidad 49):** {observaciones or 'Proceder a la carga de sobres Técnico, Administrativo y Económico en el portal oficial con al menos 24 h de margen respecto del cierre y archivar comprobante en envio/.'}\n"
    )
    acta_path = dest / "revision" / "acta_aprobacion.md"
    acta_path.write_text(acta_md, encoding="utf-8")
    generar_informe_revisor_final(codigo)
    print(f"[OK] Acta de aprobación emitida en: {acta_path}")
    return acta_path


def main() -> None:
    parser = argparse.ArgumentParser(description="Genera el informe para el Revisor Final y registra la aprobación.")
    parser.add_argument("codigo", help="Código de la licitación")
    parser.add_argument("--aprobar", action="store_true", help="Registra aprobación formal del envío (Habilidad 48)")
    parser.add_argument("--precio", type=float, default=None, help="Precio final autorizado por el Aprobador")
    parser.add_argument("--moneda", default="UF", help="Moneda del precio aprobado (UF, CLP, USD)")
    parser.add_argument("--por", default="Carlos Cristian Ávila Elgueta", help="Nombre del Revisor Final / Aprobador")
    parser.add_argument("--obs", default="", help="Observaciones o condiciones de aprobación")
    args = parser.parse_args()

    generar_informe_revisor_final(args.codigo)
    if args.aprobar:
        if args.precio is None:
            precios = leer_escenarios_costos(LIC_DIR / args.codigo)
            args.precio = precios["objetivo"]
        registrar_aprobacion(args.codigo, args.precio, args.moneda, args.por, args.obs)


if __name__ == "__main__":
    main()
