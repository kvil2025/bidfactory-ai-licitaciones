"""Consolida todas las licitaciones de `licitaciones/*/` en un tablero Excel único
(`cartera_licitaciones.xlsx`) (Habilidades 05 y 50).

Uso:
    python scripts/cartera.py
"""
from __future__ import annotations

import json
from pathlib import Path

import openpyxl
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter

ROOT = Path(__file__).resolve().parent.parent
LIC_DIR = ROOT / "licitaciones"

NAVY_FILL = PatternFill("solid", fgColor="0D2560")
GREEN_FILL = PatternFill("solid", fgColor="DCFCE7")
YELLOW_FILL = PatternFill("solid", fgColor="FEF9C3")
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


def actualizar_cartera() -> Path:
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Cartera_Licitaciones"

    ws["A1"] = "CARTERA GENERAL DE LICITACIONES — GEOLOGGIA LTDA."
    ws["A1"].font = TITLE_FONT

    headers = [
        "Código",
        "Nombre de la Licitación",
        "Mandante",
        "Portal / Canal",
        "Modalidad Contrato",
        "Fecha Cierre Ofertas",
        "Estado Global",
        "Fase Actual",
        "Habilidad Actual",
        "Decisión Go/No-Go",
        "Puntaje Simulado QA",
        "Precio Aprobado",
        "Moneda",
        "Revisor Final / Aprobador",
    ]
    for col_idx, h in enumerate(headers, start=1):
        c = ws.cell(row=3, column=col_idx, value=h)
        c.fill = NAVY_FILL
        c.font = WHITE_BOLD
        c.border = THIN_BORDER
        c.alignment = Alignment(horizontal="center", wrap_text=True)

    carpetas = sorted([d for d in LIC_DIR.iterdir() if d.is_dir() and (d / "ficha.json").exists()]) if LIC_DIR.exists() else []
    for idx, d in enumerate(carpetas, start=4):
        ficha = json.loads((d / "ficha.json").read_text(encoding="utf-8"))
        estado = json.loads((d / "estado.json").read_text(encoding="utf-8")) if (d / "estado.json").exists() else {}
        aprob = estado.get("aprobacion", {})
        rev = estado.get("revision_final", {})
        gng = estado.get("go_no_go", {})

        row_vals = [
            ficha.get("codigo", d.name),
            ficha.get("nombre", ""),
            ficha.get("mandante", ""),
            ficha.get("portal", ""),
            ficha.get("modalidad_contrato", ""),
            ficha.get("hitos", {}).get("cierre_ofertas", ""),
            estado.get("estado_global", "RECIBIDA"),
            estado.get("fase_actual", ""),
            estado.get("habilidad_actual", 1),
            gng.get("decision_aprobador", "PENDIENTE"),
            rev.get("puntaje_tecnico_simulado", ""),
            aprob.get("precio_aprobado", ""),
            aprob.get("moneda", ficha.get("moneda", "UF")),
            aprob.get("aprobador", "Carlos Ávila"),
        ]
        for col_idx, val in enumerate(row_vals, start=1):
            c = ws.cell(row=idx, column=col_idx, value=val)
            c.border = THIN_BORDER
            c.font = BODY_FONT
            if col_idx == 7:
                c.font = BOLD_FONT
                c.fill = GREEN_FILL if val in {"APROBADA", "ENVIADA", "ADJUDICADA"} else YELLOW_FILL
            if col_idx == 12 and isinstance(val, (int, float)):
                c.number_format = "#,##0.00"

    widths = [16, 42, 26, 22, 20, 20, 16, 28, 16, 18, 20, 18, 10, 24]
    for col_idx, w in enumerate(widths, start=1):
        ws.column_dimensions[get_column_letter(col_idx)].width = w

    out_xlsx = ROOT / "cartera_licitaciones.xlsx"
    wb.save(out_xlsx)
    print(f"[OK] Cartera actualizada ({len(carpetas)} licitación/es) en: {out_xlsx}")
    return out_xlsx


if __name__ == "__main__":
    actualizar_cartera()
