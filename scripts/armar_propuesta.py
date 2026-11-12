"""Compila la Propuesta Técnica en Word (`propuesta/propuesta_tecnica_<CODIGO>.docx`)
a partir de las secciones Markdown (`propuesta/secciones/*.md`), `gantt.csv` y `equipo.csv`,
y ejecuta el auditor de calidad pre-envío (`--verificar`) (Habilidades 20 a 28 y 46).

Uso:
    python scripts/armar_propuesta.py <CODIGO> [--verificar]
"""
from __future__ import annotations

import argparse
import csv
import json
import re
from datetime import datetime
from pathlib import Path

import docx
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Pt, RGBColor

ROOT = Path(__file__).resolve().parent.parent
LIC_DIR = ROOT / "licitaciones"
MODELOS_DIR = ROOT / "plantillas" / "modelos_propuesta"

NAVY_HEX = "0D2560"
SLATE_HEX = "1E293B"
ZEBRA_HEX = "F8FAFC"


def set_cell_shading(cell: docx.table._Cell, color_hex: str) -> None:
    tcPr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear")
    shd.set(qn("w:color"), "auto")
    shd.set(qn("w:fill"), color_hex)
    tcPr.append(shd)


def configurar_estilos(doc: docx.Document) -> None:
    for section in doc.sections:
        section.top_margin = Cm(2.5)
        section.bottom_margin = Cm(2.2)
        section.left_margin = Cm(2.5)
        section.right_margin = Cm(2.2)

    normal = doc.styles["Normal"]
    normal.font.name = "Calibri"
    normal.font.size = Pt(11)
    normal.font.color.rgb = RGBColor(0x1E, 0x29, 0x3B)

    for level, (size, color) in enumerate(
        [(16, RGBColor(0x0D, 0x25, 0x60)), (13, RGBColor(0x1E, 0x3A, 0x8A)), (11, RGBColor(0x0F, 0x17, 0x2A))],
        start=1,
    ):
        st = doc.styles[f"Heading {level}"]
        st.font.name = "Calibri"
        st.font.size = Pt(size)
        st.font.bold = True
        st.font.color.rgb = color


def agregar_tabla_estilizada(doc: docx.Document, headers: list[str], rows: list[list[str]]) -> None:
    table = doc.add_table(rows=1, cols=len(headers))
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.style = "Table Grid"
    hdr_cells = table.rows[0].cells
    for idx, h in enumerate(headers):
        hdr_cells[idx].text = h
        set_cell_shading(hdr_cells[idx], NAVY_HEX)
        for p in hdr_cells[idx].paragraphs:
            for r in p.runs:
                r.font.bold = True
                r.font.size = Pt(9.5)
                r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)

    for r_idx, row_data in enumerate(rows):
        cells = table.add_row().cells
        for c_idx, val in enumerate(row_data):
            cells[c_idx].text = str(val)
            if r_idx % 2 == 1:
                set_cell_shading(cells[c_idx], ZEBRA_HEX)
            for p in cells[c_idx].paragraphs:
                for r in p.runs:
                    r.font.size = Pt(9.5)
    doc.add_paragraph()


def agregar_markdown_a_doc(doc: docx.Document, md_text: str) -> None:
    for raw_line in md_text.splitlines():
        line = raw_line.strip()
        if not line:
            continue
        if line.startswith("# "):
            doc.add_heading(line[2:].strip(), level=1)
        elif line.startswith("## "):
            doc.add_heading(line[3:].strip(), level=2)
        elif line.startswith("### "):
            doc.add_heading(line[4:].strip(), level=3)
        elif line.startswith("- "):
            p = doc.add_paragraph(style="List Bullet")
            _agregar_runs_con_negrita(p, line[2:].strip())
        else:
            p = doc.add_paragraph()
            _agregar_runs_con_negrita(p, line)


def _agregar_runs_con_negrita(p: docx.text.paragraph.Paragraph, texto: str) -> None:
    partes = re.split(r"(\*\*[^*]+\*\*)", texto)
    for parte in partes:
        if parte.startswith("**") and parte.endswith("**"):
            r = p.add_run(parte[2:-2])
            r.bold = True
        else:
            p.add_run(parte)


def compilar_propuesta(codigo: str) -> Path:
    dest = LIC_DIR / codigo
    ficha = json.loads((dest / "ficha.json").read_text(encoding="utf-8"))

    # Si el usuario dejó un archivo Word maestro en plantillas/modelos_propuesta/plantilla_base_geologgia.docx,
    # se usa como base de estilos, membrete, encabezados y pies de página corporativos.
    MODELOS_DIR.mkdir(parents=True, exist_ok=True)
    plantilla_corporativa = MODELOS_DIR / "plantilla_base_geologgia.docx"
    if plantilla_corporativa.exists():
        doc = docx.Document(plantilla_corporativa)
        print(f"[INFO] Usando plantilla corporativa base: {plantilla_corporativa.name}")
    else:
        doc = docx.Document()
    configurar_estilos(doc)

    # Encabezado institucional
    header = doc.sections[0].header
    hp = header.paragraphs[0]
    hp.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    hrun = hp.add_run(f"GEOLOGGIA LTDA. | Propuesta Técnica · {codigo} · {ficha.get('mandante', '')}")
    hrun.font.size = Pt(8.5)
    hrun.font.color.rgb = RGBColor(0x64, 0x74, 0x8B)

    # Portada
    p_top = doc.add_paragraph()
    p_top.alignment = WD_ALIGN_PARAGRAPH.LEFT
    r_emp = p_top.add_run("GEOLOGGIA LTDA. — CONSULTORÍA EN GEOLOGÍA, GEOTECNIA Y OBRAS SUBTERRÁNEAS")
    r_emp.bold = True
    r_emp.font.size = Pt(11)
    r_emp.font.color.rgb = RGBColor(0x0D, 0x25, 0x60)

    p_tit = doc.add_paragraph()
    p_tit.paragraph_format.space_before = Pt(28)
    r_tit = p_tit.add_run(f"PROPUESTA TÉCNICA\n{ficha.get('nombre', '')}")
    r_tit.bold = True
    r_tit.font.size = Pt(20)
    r_tit.font.color.rgb = RGBColor(0x0D, 0x25, 0x60)

    agregar_tabla_estilizada(
        doc,
        ["Campo", "Detalle de la Oferta Técnica"],
        [
            ["Código de Licitación", codigo],
            ["Mandante", ficha.get("mandante", "")],
            ["Portal / Modalidad", f"{ficha.get('portal', '')} | {ficha.get('modalidad_contrato', '')}"],
            ["Oferente", "Geologgia Ltda. (www.geologgia.cl)"],
            ["Director de Proyecto", "Carlos Cristian Ávila Elgueta (Geólogo, +20 años exp.)"],
            ["Fecha de Emisión", datetime.now().strftime("%Y-%m-%d")],
        ],
    )
    doc.add_page_break()

    # Secciones Markdown en orden
    sec_dir = dest / "propuesta" / "secciones"
    for md_file in sorted(sec_dir.glob("*.md")):
        agregar_markdown_a_doc(doc, md_file.read_text(encoding="utf-8"))

        # Insertar tablas de Gantt y Equipo justo después de 03_plan_trabajo_equipo.md
        if md_file.name.startswith("03"):
            gantt_csv = dest / "propuesta" / "gantt.csv"
            if gantt_csv.exists():
                doc.add_heading("3.3 Carta Gantt de Actividades y Entregables", level=2)
                with gantt_csv.open(encoding="utf-8") as f:
                    reader = list(csv.reader(f))
                    if len(reader) > 1:
                        agregar_tabla_estilizada(
                            doc,
                            ["#", "Actividad", "Semana Inicio", "Duración (sem)", "Responsable", "Entregable Verificable"],
                            reader[1:],
                        )

            equipo_csv = dest / "propuesta" / "equipo.csv"
            if equipo_csv.exists():
                doc.add_heading("3.4 Nómina de Equipo Profesional Propuesto", level=2)
                with equipo_csv.open(encoding="utf-8") as f:
                    reader = list(csv.reader(f))
                    if len(reader) > 1:
                        agregar_tabla_estilizada(
                            doc,
                            ["Rol en el Proyecto", "Profesional", "Profesión", "Años Exp.", "Dedicación", "Track Record Relevante"],
                            reader[1:],
                        )

    out_docx = dest / "propuesta" / f"propuesta_tecnica_{codigo}.docx"
    doc.save(out_docx)
    print(f"[OK] Propuesta Técnica Word generada en: {out_docx}")
    return out_docx


def verificar_propuesta(codigo: str) -> dict[str, list[str]]:
    dest = LIC_DIR / codigo
    sec_dir = dest / "propuesta" / "secciones"
    textos = "\n".join(p.read_text(encoding="utf-8") for p in sorted(sec_dir.glob("*.md")))

    marcadores_pendientes = re.findall(r"\[COMPLETAR[^\]]*\]|\bTODO\b|\bTBD\b", textos, flags=re.IGNORECASE)
    posibles_precios_filtrados = re.findall(
        r"(?:precio\s+total|oferta\s+econ[oó]mica|valor\s+total)\s*[:=]?\s*[\d.,]+\s*(?:UF|CLP|USD)",
        textos,
        flags=re.IGNORECASE,
    )

    hallazgos = {
        "marcadores_pendientes": marcadores_pendientes,
        "posibles_precios_en_sobre_tecnico": posibles_precios_filtrados,
    }
    reporte_path = dest / "revision" / "verificacion_estilo_y_formato.md"
    lineas = [
        f"# Verificación Automática de Propuesta Técnica (Habilidad 46) — `{codigo}`",
        "",
        f"- **Marcadores `[COMPLETAR]` / `TODO` encontrados:** {len(marcadores_pendientes)}",
        *(f"  - `{m}`" for m in marcadores_pendientes),
        f"- **Alertas de posible filtración de precio en sobre técnico:** {len(posibles_precios_filtrados)}",
        *(f"  - `{p}`" for p in posibles_precios_filtrados),
        "",
        "**Resultado:** "
        + ("APROBADO SIN OBSERVACIONES DE FORMATO" if not (marcadores_pendientes or posibles_precios_filtrados) else "REQUIERE CORRECCIÓN ANTES DEL ENVÍO"),
    ]
    reporte_path.write_text("\n".join(lineas) + "\n", encoding="utf-8")
    print(f"[QA] Verificación completada → {reporte_path}")
    return hallazgos


def main() -> None:
    parser = argparse.ArgumentParser(description="Compila la propuesta técnica en Word y verifica su calidad.")
    parser.add_argument("codigo", help="Código de la licitación")
    parser.add_argument("--verificar", action="store_true", help="Ejecuta el verificador QA (Habilidad 46)")
    args = parser.parse_args()
    compilar_propuesta(args.codigo)
    if args.verificar:
        verificar_propuesta(args.codigo)


if __name__ == "__main__":
    main()
