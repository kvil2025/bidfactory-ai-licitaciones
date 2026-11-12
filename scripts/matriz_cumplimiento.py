"""Genera y actualiza la Matriz de Cumplimiento en Excel (`matriz_cumplimiento.xlsx`)
con fórmulas dinámicas, formato condicional visual y hoja de Criterios de Evaluación (Habilidades 09, 10, 19, 41).

Uso:
    python scripts/matriz_cumplimiento.py <CODIGO> [--resumen]
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import openpyxl
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.datavalidation import DataValidation

ROOT = Path(__file__).resolve().parent.parent
LIC_DIR = ROOT / "licitaciones"

NAVY_FILL = PatternFill("solid", fgColor="0D2560")
SUBHEADER_FILL = PatternFill("solid", fgColor="1E3A8A")
ZEBRA_FILL = PatternFill("solid", fgColor="F8FAFC")
GREEN_FILL = PatternFill("solid", fgColor="DCFCE7")
YELLOW_FILL = PatternFill("solid", fgColor="FEF9C3")
RED_FILL = PatternFill("solid", fgColor="FEE2E2")

WHITE_BOLD = Font(name="Calibri", size=11, bold=True, color="FFFFFF")
TITLE_FONT = Font(name="Calibri", size=14, bold=True, color="0D2560")
BODY_FONT = Font(name="Calibri", size=10, color="0F172A")
BOLD_FONT = Font(name="Calibri", size=10, bold=True, color="0F172A")

THIN_BORDER = Border(
    left=Side(style="thin", color="CBD5E1"),
    right=Side(style="thin", color="CBD5E1"),
    top=Side(style="thin", color="CBD5E1"),
    bottom=Side(style="thin", color="CBD5E1"),
)


def generar_matriz_excel(codigo: str) -> Path:
    dest = LIC_DIR / codigo
    ficha = json.loads((dest / "ficha.json").read_text(encoding="utf-8"))
    req_data = json.loads((dest / "analisis" / "requisitos.json").read_text(encoding="utf-8"))
    requisitos = req_data.get("requisitos", [])
    criterios = req_data.get("criterios", [])

    wb = openpyxl.Workbook()

    # ---------------- HOJA 1: MATRIZ DE CUMPLIMIENTO ----------------
    ws = wb.active
    ws.title = "Matriz_Cumplimiento"
    ws.views.sheetView[0].showGridLines = True

    ws["A1"] = f"MATRIZ DE CUMPLIMIENTO INTEGRAL — {codigo} · {ficha.get('nombre', '')}"
    ws["A1"].font = TITLE_FONT
    ws["A2"] = f"Mandante: {ficha.get('mandante', '')} | Cierre: {ficha.get('hitos', {}).get('cierre_ofertas', '')}"
    ws["A2"].font = BOLD_FONT

    headers = [
        "ID",
        "Categoría",
        "Requisito Exigido en las Bases",
        "Documento Fuente",
        "Numeral / Página",
        "Obligatorio",
        "Causal Inadmisibilidad",
        "Rol Responsable",
        "Sección / Anexo de la Oferta donde se Responde",
        "Estado",
        "Evidencia / Observaciones de Revisión QA",
    ]
    header_row = 4
    for col_idx, h in enumerate(headers, start=1):
        cell = ws.cell(row=header_row, column=col_idx, value=h)
        cell.fill = NAVY_FILL
        cell.font = WHITE_BOLD
        cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        cell.border = THIN_BORDER
    ws.row_dimensions[header_row].height = 28

    for idx, r in enumerate(requisitos, start=header_row + 1):
        estado = r.get("estado", "Pendiente")
        row_vals = [
            r.get("id", f"REQ-{idx:03d}"),
            r.get("categoria", "Técnico"),
            r.get("requisito", ""),
            r.get("documento_fuente", ""),
            r.get("seccion_pagina", ""),
            "SÍ" if r.get("obligatorio", True) else "NO",
            "SÍ" if r.get("causal_inadmisibilidad", False) else "NO",
            r.get("responsable", ""),
            r.get("documento_oferta", ""),
            estado,
            r.get("evidencia_observaciones", ""),
        ]
        for col_idx, val in enumerate(row_vals, start=1):
            c = ws.cell(row=idx, column=col_idx, value=val)
            c.font = BODY_FONT
            c.border = THIN_BORDER
            c.alignment = Alignment(
                horizontal="center" if col_idx in {1, 2, 4, 6, 7, 10} else "left",
                vertical="top",
                wrap_text=True,
            )
            if idx % 2 == 1:
                c.fill = ZEBRA_FILL
            if col_idx == 10:
                if estado == "Cumple":
                    c.fill = GREEN_FILL
                    c.font = BOLD_FONT
                elif estado in {"En curso", "Cumple con desviación"}:
                    c.fill = YELLOW_FILL
                    c.font = BOLD_FONT
                else:
                    c.fill = RED_FILL
                    c.font = BOLD_FONT
            if col_idx == 7 and val == "SÍ":
                c.font = Font(name="Calibri", size=10, bold=True, color="B91C1C")
        ws.row_dimensions[idx].height = 36

    last_row = max(header_row + len(requisitos), header_row + 1)
    dv = DataValidation(
        type="list",
        formula1='"Cumple,En curso,Cumple con desviación,Pendiente,No cumple"',
        allow_blank=False,
    )
    ws.add_data_validation(dv)
    dv.add(f"J5:J{last_row + 20}")

    widths = [11, 18, 48, 16, 18, 13, 18, 22, 34, 20, 42]
    for col_idx, w in enumerate(widths, start=1):
        ws.column_dimensions[get_column_letter(col_idx)].width = w
    ws.freeze_panes = "A5"

    # ---------------- HOJA 2: RESUMEN EJECUTIVO (FÓRMULAS) ----------------
    ws_res = wb.create_sheet("Resumen_QA")
    ws_res["A1"] = f"RESUMEN DE CUMPLIMIENTO Y CONTROL DE INADMISIBILIDAD — {codigo}"
    ws_res["A1"].font = TITLE_FONT

    res_headers = ["Indicador de Control", "Cantidad / Valor", "Fórmula / Criterio"]
    for col_idx, h in enumerate(res_headers, start=1):
        c = ws_res.cell(row=3, column=col_idx, value=h)
        c.fill = NAVY_FILL
        c.font = WHITE_BOLD
        c.border = THIN_BORDER

    metricas = [
        ("Total de Requisitos Identificados", f"=COUNTA(Matriz_Cumplimiento!A5:A{last_row})", "Conteo total en matriz"),
        ("Requisitos en estado 'Cumple'", f'=COUNTIF(Matriz_Cumplimiento!J5:J{last_row},"Cumple")', "Listos y verificados"),
        ("Requisitos 'En curso' o 'Pendiente'", f'=COUNTIF(Matriz_Cumplimiento!J5:J{last_row},"En curso")+COUNTIF(Matriz_Cumplimiento!J5:J{last_row},"Pendiente")', "Requieren cierre antes de Habilidad 47"),
        ("Requisitos con Desviación Declarada", f'=COUNTIF(Matriz_Cumplimiento!J5:J{last_row},"Cumple con desviación")', "Deben ser autorizados por Revisor Final"),
        ("Requisitos en estado 'No cumple'", f'=COUNTIF(Matriz_Cumplimiento!J5:J{last_row},"No cumple")', "Bloqueante si es causal de inadmisibilidad"),
        ("Causales de Inadmisibilidad Pendientes / No Cumple", f'=COUNTIFS(Matriz_Cumplimiento!G5:G{last_row},"SÍ",Matriz_Cumplimiento!J5:J{last_row},"<>Cumple")', "DEBE SER 0 ANTES DE ENVIAR LA OFERTA"),
        ("% de Cumplimiento Verificado", "=IF(B4>0,B5/B4,0)", "Meta pre-envío: 100%"),
    ]
    for r_idx, (nombre_m, formula, crit) in enumerate(metricas, start=4):
        c1 = ws_res.cell(row=r_idx, column=1, value=nombre_m)
        c2 = ws_res.cell(row=r_idx, column=2, value=formula)
        c3 = ws_res.cell(row=r_idx, column=3, value=crit)
        for c in (c1, c2, c3):
            c.border = THIN_BORDER
            c.font = BOLD_FONT if r_idx in {9, 10} else BODY_FONT
        if r_idx == 10:
            c2.number_format = "0.0%"
            c2.fill = GREEN_FILL
        elif r_idx == 9:
            c2.fill = YELLOW_FILL

    ws_res.column_dimensions["A"].width = 48
    ws_res.column_dimensions["B"].width = 20
    ws_res.column_dimensions["C"].width = 45

    # ---------------- HOJA 3: CRITERIOS DE EVALUACIÓN Y SIMULADOR ----------------
    ws_crit = wb.create_sheet("Criterios_Evaluacion")
    ws_crit["A1"] = f"PAUTA DE EVALUACIÓN Y SIMULADOR DE PUNTAJE (HABILIDADES 10 Y 45) — {codigo}"
    ws_crit["A1"].font = TITLE_FONT

    crit_headers = [
        "ID",
        "Criterio de Evaluación",
        "Ponderación (%)",
        "Puntaje Máximo",
        "Regla de Puntaje en Bases",
        "Estrategia Ganadora Geologgia",
        "Puntaje Simulado QA (0-100)",
        "Puntaje Ponderado",
    ]
    for col_idx, h in enumerate(crit_headers, start=1):
        c = ws_crit.cell(row=3, column=col_idx, value=h)
        c.fill = SUBHEADER_FILL
        c.font = WHITE_BOLD
        c.border = THIN_BORDER

    for i, cr in enumerate(criterios, start=4):
        vals = [
            cr.get("id", f"CRIT-{i-3:02d}"),
            cr.get("criterio", ""),
            cr.get("ponderacion_pct", 0) / 100.0,
            cr.get("puntaje_max", 100),
            cr.get("regla_puntaje", ""),
            cr.get("estrategia_geologgia", ""),
            cr.get("puntaje_simulado", 90),
            f"=C{i}*G{i}",
        ]
        for col_idx, v in enumerate(vals, start=1):
            cell = ws_crit.cell(row=i, column=col_idx, value=v)
            cell.border = THIN_BORDER
            cell.font = BODY_FONT
            cell.alignment = Alignment(vertical="top", wrap_text=True)
            if col_idx == 3:
                cell.number_format = "0.0%"
            elif col_idx == 8:
                cell.number_format = "0.00"
                cell.font = BOLD_FONT

    tot_row = 4 + len(criterios)
    ws_crit.cell(row=tot_row, column=2, value="TOTAL PONDERADO ESTIMADO").font = BOLD_FONT
    c_pond = ws_crit.cell(row=tot_row, column=3, value=f"=SUM(C4:C{tot_row-1})")
    c_pond.number_format = "0.0%"
    c_pond.font = BOLD_FONT
    c_tot = ws_crit.cell(row=tot_row, column=8, value=f"=SUM(H4:H{tot_row-1})")
    c_tot.number_format = "0.00"
    c_tot.font = BOLD_FONT
    c_tot.fill = GREEN_FILL

    for col_idx, w in enumerate([12, 32, 16, 15, 38, 42, 22, 18], start=1):
        ws_crit.column_dimensions[get_column_letter(col_idx)].width = w

    out_xlsx = dest / "analisis" / "matriz_cumplimiento.xlsx"
    wb.save(out_xlsx)
    print(f"[OK] Matriz de cumplimiento generada en: {out_xlsx}")
    return out_xlsx


def imprimir_resumen(codigo: str) -> None:
    dest = LIC_DIR / codigo
    req_data = json.loads((dest / "analisis" / "requisitos.json").read_text(encoding="utf-8"))
    reqs = req_data.get("requisitos", [])
    total = len(reqs)
    cumple = sum(1 for r in reqs if r.get("estado") == "Cumple")
    inadm_pend = [
        r["id"]
        for r in reqs
        if r.get("causal_inadmisibilidad") and r.get("estado") != "Cumple"
    ]
    print(
        f"[RESUMEN MATRIZ {codigo}] Total={total} | Cumple={cumple} ({(cumple/total*100 if total else 0):.1f}%) "
        f"| Causales inadmisibilidad pendientes={len(inadm_pend)} {inadm_pend}"
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="Genera la matriz de cumplimiento en Excel.")
    parser.add_argument("codigo", help="Código de la licitación")
    parser.add_argument("--resumen", action="store_true", help="Imprime resumen de cumplimiento en consola")
    args = parser.parse_args()
    generar_matriz_excel(args.codigo)
    if args.resumen:
        imprimir_resumen(args.codigo)


if __name__ == "__main__":
    main()
