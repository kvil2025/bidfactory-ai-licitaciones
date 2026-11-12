"""Genera la planilla de Propuesta Económica y APU (`propuesta/economica/costos.xlsx`)
con hojas de Resumen & Escenarios (Objetivo / Agresivo / Conservador), HH por Rol,
Costos Directos (sondajes, laboratorio, terreno) y Formulario Oficial (Habilidades 29 a 34).

Uso:
    python scripts/plantilla_costos.py <CODIGO>
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import openpyxl
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter

ROOT = Path(__file__).resolve().parent.parent
LIC_DIR = ROOT / "licitaciones"

NAVY_FILL = PatternFill("solid", fgColor="0D2560")
ACCENT_FILL = PatternFill("solid", fgColor="1E3A8A")
SOFT_FILL = PatternFill("solid", fgColor="F1F5F9")
GREEN_FILL = PatternFill("solid", fgColor="DCFCE7")
WHITE_BOLD = Font(name="Calibri", size=11, bold=True, color="FFFFFF")
TITLE_FONT = Font(name="Calibri", size=14, bold=True, color="0D2560")
BOLD_FONT = Font(name="Calibri", size=10, bold=True, color="0F172A")
BODY_FONT = Font(name="Calibri", size=10, color="0F172A")

THIN_BORDER = Border(
    left=Side(style="thin", color="CBD5E1"),
    right=Side(style="thin", color="CBD5E1"),
    top=Side(style="thin", color="CBD5E1"),
    bottom=Side(style="thin", color="CBD5E1"),
)


def generar_costos_excel(codigo: str) -> Path:
    dest = LIC_DIR / codigo
    ficha = json.loads((dest / "ficha.json").read_text(encoding="utf-8"))
    wb = openpyxl.Workbook()

    # ---------------- HOJA 1: HH PROFESIONALES (HABILIDAD 30) ----------------
    ws_hh = wb.active
    ws_hh.title = "HH_Profesionales"
    ws_hh["A1"] = f"ESTIMACIÓN DE HORAS HOMBRE (HH) POR ROL Y ETAPA — {codigo}"
    ws_hh["A1"].font = TITLE_FONT

    headers_hh = [
        "Código Rol",
        "Cargo / Especialista",
        "Tarifa Costo (UF/HH)",
        "Etapa 1: Gabinete Inicial",
        "Etapa 2: Campaña Terreno",
        "Etapa 3: Modelamiento e Informe",
        "Total HH",
        "Costo Total HH (UF)",
    ]
    for col_idx, h in enumerate(headers_hh, start=1):
        c = ws_hh.cell(row=3, column=col_idx, value=h)
        c.fill = NAVY_FILL
        c.font = WHITE_BOLD
        c.border = THIN_BORDER
        c.alignment = Alignment(horizontal="center", wrap_text=True)

    if "CACHAPOAL" in codigo.upper() or "riesgo" in ficha.get("nombre", "").lower():
        roles_base = [
            ("DIR-01", "Director de Proyecto y Especialista Hidroeléctrico (Cristian Ávila)", 2.40, 16, 40, 28),
            ("JPR-01", "Especialista Senior en Peligros Geológicos y Geomorfología", 1.90, 28, 45, 52),
            ("ESP-01", "Especialista en Hidroclimatología y Cambio Climático (ARCliM/CMIP6)", 1.75, 16, 0, 44),
            ("GEO-01", "Geólogo Geotécnico de Terreno y Estabilidad de Taludes", 1.30, 16, 45, 36),
            ("SIG-01", "Especialista GIS, Teledetección DEM y Geodatabase", 0.95, 24, 0, 56),
        ]
    else:
        roles_base = [
            ("DIR-01", "Director de Proyecto / Revisor Senior (Cristian Ávila)", 2.40, 16, 20, 24),
            ("JPR-01", "Jefe de Terreno / Geólogo Geotécnico Senior", 1.90, 24, 80, 40),
            ("GEO-01", "Geólogo de Terreno / Logueo y Mapeo", 1.30, 16, 120, 32),
            ("ESP-01", "Especialista Mecánica de Rocas / Estabilidad", 1.75, 12, 0, 48),
            ("SIG-01", "Especialista GIS / Cartografía / Modelo 3D", 0.95, 20, 10, 40),
            ("HSE-01", "Asesor Prevención de Riesgos (APR)", 1.10, 12, 20, 8),
        ]
    for idx, (cod, cargo, tarifa, e1, e2, e3) in enumerate(roles_base, start=4):
        vals = [cod, cargo, tarifa, e1, e2, e3, f"=SUM(D{idx}:F{idx})", f"=C{idx}*G{idx}"]
        for col_idx, v in enumerate(vals, start=1):
            c = ws_hh.cell(row=idx, column=col_idx, value=v)
            c.border = THIN_BORDER
            c.font = BODY_FONT
            if col_idx in {3, 8}:
                c.number_format = "#,##0.00"
            elif col_idx in {4, 5, 6, 7}:
                c.number_format = "#,##0"

    tot_hh_row = 4 + len(roles_base)
    ws_hh.cell(row=tot_hh_row, column=2, value="TOTAL HH Y COSTO PROFESIONAL (UF)").font = BOLD_FONT
    for col_idx in range(4, 9):
        col_let = get_column_letter(col_idx)
        c = ws_hh.cell(row=tot_hh_row, column=col_idx, value=f"=SUM({col_let}4:{col_let}{tot_hh_row-1})")
        c.font = BOLD_FONT
        c.fill = SOFT_FILL
        c.border = THIN_BORDER
        c.number_format = "#,##0.00" if col_idx == 8 else "#,##0"

    for col_idx, w in enumerate([14, 42, 18, 18, 18, 20, 14, 20], start=1):
        ws_hh.column_dimensions[get_column_letter(col_idx)].width = w

    # ---------------- HOJA 2: COSTOS DIRECTOS Y SUBCONTRATOS (HABILIDAD 31) ----------------
    ws_cd = wb.create_sheet("Costos_Directos")
    ws_cd["A1"] = f"COSTOS DIRECTOS DE TERRENO, LABORATORIO Y SUBCONTRATOS — {codigo}"
    ws_cd["A1"].font = TITLE_FONT

    headers_cd = ["Ítem", "Categoría", "Descripción", "Unidad", "Cantidad", "P. Unitario (UF)", "Subtotal (UF)", "Proveedor / Respaldo"]
    for col_idx, h in enumerate(headers_cd, start=1):
        c = ws_cd.cell(row=3, column=col_idx, value=h)
        c.fill = NAVY_FILL
        c.font = WHITE_BOLD
        c.border = THIN_BORDER

    if "CACHAPOAL" in codigo.upper() or "riesgo" in ficha.get("nombre", "").lower():
        items_cd = [
            ("CD-01", "Terreno", "Camioneta 4x4 equipada para cordillera (Valle del Alto Cachapoal, 6 días)", "Día", 6, 2.10, "Tarifario interno Geologgia"),
            ("CD-02", "Terreno", "Combustible, peajes y traslados a faenas Alto Cachapoal", "Día", 6, 0.95, "Estimación ruta Machalí / Coya / Chacayes"),
            ("CD-03", "Terreno", "Alojamiento y alimentación cuadrilla en terreno (3 especialistas x 5 noches)", "Persona-día", 15, 1.85, "Zona Coya / Machalí"),
            ("CD-04", "Geomática", "Procesamiento satelital multitemporal, DEM alta resolución y coberturas ARCliM/CMIP6", "Glosa", 1, 14.00, "Gabinete Geomática Geologgia"),
            ("CD-05", "Seguridad", "Acreditación HSE, seguros de terreno y equipamiento de montaña/radios", "Glosa", 1, 6.50, "Estándar #PacificHydroWay"),
        ]
    else:
        items_cd = [
            ("CD-01", "Terreno", "Arriendo Camioneta 4x4 equipada estándar minero", "Día", 14, 2.10, "Tarifario interno Geologgia"),
            ("CD-02", "Terreno", "Combustible, peajes y logística de ruta", "Día", 14, 0.85, "Estimación ruta faena"),
            ("CD-03", "Terreno", "Alojamiento y alimentación cuadrilla en terreno", "Persona-día", 42, 1.90, "3 profesionales x 14 días"),
            ("CD-04", "Acreditación", "Exámenes preocupacionales altura geográfica + EPP específico", "Persona", 4, 4.50, "Mutualidad / Centro médico"),
            ("CD-05", "Laboratorio", "Ensayos de mecánica de rocas (UCS, carga puntual Is50, propiedades índices)", "Glosa", 1, 45.00, "Cotización Laboratorio Geotécnico"),
            ("CD-06", "Financiero", "Comisión emisión Garantía de Seriedad y Fiel Cumplimiento", "Glosa", 1, 4.00, "Banco"),
        ]
    for idx, (it, cat, desc, unid, cant, pu, prov) in enumerate(items_cd, start=4):
        vals = [it, cat, desc, unid, cant, pu, f"=E{idx}*F{idx}", prov]
        for col_idx, v in enumerate(vals, start=1):
            c = ws_cd.cell(row=idx, column=col_idx, value=v)
            c.border = THIN_BORDER
            c.font = BODY_FONT
            if col_idx in {6, 7}:
                c.number_format = "#,##0.00"

    tot_cd_row = 4 + len(items_cd)
    ws_cd.cell(row=tot_cd_row, column=3, value="TOTAL COSTOS DIRECTOS NO-HH (UF)").font = BOLD_FONT
    c_tot_cd = ws_cd.cell(row=tot_cd_row, column=7, value=f"=SUM(G4:G{tot_cd_row-1})")
    c_tot_cd.font = BOLD_FONT
    c_tot_cd.fill = SOFT_FILL
    c_tot_cd.border = THIN_BORDER
    c_tot_cd.number_format = "#,##0.00"

    for col_idx, w in enumerate([12, 16, 46, 14, 12, 16, 18, 30], start=1):
        ws_cd.column_dimensions[get_column_letter(col_idx)].width = w

    # ---------------- HOJA 3: RESUMEN Y ANÁLISIS DE SENSIBILIDAD (HABILIDADES 32, 33, 34) ----------------
    ws_res = wb.create_sheet("Resumen_y_Escenarios")
    ws_res["A1"] = f"RESUMEN ECONÓMICO Y ESCENARIOS DE DECISIÓN DEL APROBADOR — {codigo}"
    ws_res["A1"].font = TITLE_FONT

    ws_res["A3"] = "Concepto de Estructura de Precio"
    ws_res["B3"] = "% / Parámetro"
    ws_res["C3"] = "Escenario Agresivo (UF)"
    ws_res["D3"] = "Escenario Objetivo (UF)"
    ws_res["E3"] = "Escenario Conservador (UF)"
    for col_idx in range(1, 6):
        c = ws_res.cell(row=3, column=col_idx)
        c.fill = ACCENT_FILL
        c.font = WHITE_BOLD
        c.border = THIN_BORDER

    filas_res = [
        ("1. Costo Directo HH Profesionales", "", f"=HH_Profesionales!H{tot_hh_row}", f"=HH_Profesionales!H{tot_hh_row}", f"=HH_Profesionales!H{tot_hh_row}"),
        ("2. Costos Directos Terreno, Laboratorio y Subcontratos", "", f"=Costos_Directos!G{tot_cd_row}", f"=Costos_Directos!G{tot_cd_row}", f"=Costos_Directos!G{tot_cd_row}"),
        ("SUBTOTAL COSTO DIRECTO (CD)", "", "=SUM(C4:C5)", "=SUM(D4:D5)", "=SUM(E4:E5)"),
        ("3. Gastos Generales (GG sobre CD)", 0.12, "=C6*$B7", "=D6*$B7", "=E6*$B7"),
        ("4. Contingencia por Riesgo Técnico/Contractual (3% / 6% / 10%)", 0.06, "=C6*0.03", "=D6*$B8", "=E6*0.10"),
        ("COSTO TOTAL DEL PROYECTO (CD + GG + Contingencia)", "", "=SUM(C6:C8)", "=SUM(D6:D8)", "=SUM(E6:E8)"),
        ("5. Utilidad (12% Agresivo / 18% Objetivo / 25% Conservador)", 0.18, "=C9*0.12", "=D9*$B10", "=E9*0.25"),
        ("PRECIO NETO OFERTA (UF sin IVA)", "", "=C9+C10", "=D9+D10", "=E9+E10"),
        ("Margen Bruto sobre Venta (%)", "", "=(C11-C6)/C11", "=(D11-D6)/D11", "=(E11-E6)/E11"),
    ]
    for r_idx, row_vals in enumerate(filas_res, start=4):
        for col_idx, v in enumerate(row_vals, start=1):
            c = ws_res.cell(row=r_idx, column=col_idx, value=v)
            c.border = THIN_BORDER
            c.font = BOLD_FONT if r_idx in {6, 9, 11, 12} else BODY_FONT
            if col_idx == 2 and isinstance(v, float):
                c.number_format = "0.0%"
            elif col_idx in {3, 4, 5}:
                c.number_format = "0.0%" if r_idx == 12 else "#,##0.00"
            if r_idx == 11:
                c.fill = GREEN_FILL if col_idx == 4 else SOFT_FILL

    for col_idx, w in enumerate([48, 16, 22, 22, 24], start=1):
        ws_res.column_dimensions[get_column_letter(col_idx)].width = w

    # Poner Resumen como primera pestaña visible al abrir
    wb._sheets = [ws_res, ws_hh, ws_cd]

    out_xlsx = dest / "propuesta" / "economica" / "costos.xlsx"
    wb.save(out_xlsx)
    print(f"[OK] Planilla de costos y escenarios generada en: {out_xlsx}")
    return out_xlsx


def main() -> None:
    parser = argparse.ArgumentParser(description="Genera la planilla de costos en Excel.")
    parser.add_argument("codigo", help="Código de la licitación")
    args = parser.parse_args()
    generar_costos_excel(args.codigo)


if __name__ == "__main__":
    main()
