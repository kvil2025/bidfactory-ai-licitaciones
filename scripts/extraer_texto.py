"""Extrae texto estructurado de todos los documentos en `licitaciones/<CODIGO>/bases/` (PDF, DOCX, TXT, MD)
y detecta menciones a Anexos para alertar si falta algún archivo adjunto (Habilidades 02, 07, 08).

Uso:
    python scripts/extraer_texto.py <CODIGO>
"""
from __future__ import annotations

import argparse
import re
import zipfile
from pathlib import Path

import docx
import fitz  # PyMuPDF
import openpyxl

ROOT = Path(__file__).resolve().parent.parent
LIC_DIR = ROOT / "licitaciones"


def extraer_pdf(path: Path) -> str:
    doc = fitz.open(path)
    paginas: list[str] = []
    for i, page in enumerate(doc, start=1):
        paginas.append(f"--- [Página {i}] ---\n{page.get_text('text')}")
    doc.close()
    return "\n".join(paginas)


def extraer_docx(path: Path) -> str:
    d = docx.Document(path)
    partes: list[str] = []
    for p in d.paragraphs:
        if p.text.strip():
            partes.append(p.text)
    for idx, t in enumerate(d.tables, start=1):
        partes.append(f"\n[Tabla {idx}]")
        for row in t.rows:
            partes.append(" | ".join(c.text.strip().replace("\n", " ") for c in row.cells))
    return "\n".join(partes)


def extraer_xlsx(path: Path) -> str:
    wb = openpyxl.load_workbook(path, data_only=True)
    partes: list[str] = []
    for sname in wb.sheetnames:
        ws = wb[sname]
        partes.append(f"--- [Hoja Excel: {sname}] ---")
        for row in ws.iter_rows(values_only=True):
            vals = [str(v).strip() for v in row if v is not None and str(v).strip() != ""]
            if vals:
                partes.append(" | ".join(vals))
    return "\n".join(partes)


def descomprimir_zips_en_bases(bases_dir: Path) -> None:
    for zpath in list(bases_dir.rglob("*.zip")):
        extract_dir = zpath.parent / zpath.stem
        if not extract_dir.exists():
            try:
                with zipfile.ZipFile(zpath, "r") as zf:
                    zf.extractall(extract_dir)
                print(f"[ZIP] Descomprimido: {zpath.name} -> {extract_dir.name}/")
            except Exception as e:
                print(f"[WARN] No se pudo descomprimir {zpath.name}: {e}")


def procesar_bases(codigo: str) -> None:
    dest = LIC_DIR / codigo
    bases_dir = dest / "bases"
    out_dir = dest / "analisis" / "texto"
    out_dir.mkdir(parents=True, exist_ok=True)

    descomprimir_zips_en_bases(bases_dir)

    archivos = sorted(
        [
            p
            for p in bases_dir.rglob("*")
            if p.is_file() and p.name not in {"PENDIENTES.md", "INVENTARIO_Y_FALTANTES.md"}
        ]
    )
    anexos_citados: set[str] = set()
    resumen_archivos: list[str] = []

    for arch in archivos:
        ext = arch.suffix.lower()
        texto = ""
        try:
            if ext == ".pdf":
                texto = extraer_pdf(arch)
            elif ext == ".docx":
                texto = extraer_docx(arch)
            elif ext in {".xlsx", ".xlsm"}:
                texto = extraer_xlsx(arch)
            elif ext in {".txt", ".md", ".csv", ".kml"}:
                texto = arch.read_text(encoding="utf-8", errors="replace")
            else:
                continue
        except Exception as e:
            texto = f"[Error extrayendo {arch.name}: {e}]"

        rel_name = arch.relative_to(bases_dir)
        safe_stem = "__".join(rel_name.with_suffix("").parts)
        out_txt = out_dir / f"{safe_stem}.txt"
        out_txt.write_text(texto, encoding="utf-8")
        resumen_archivos.append(f"- `{rel_name}` → `{out_txt.name}` ({len(texto):,} caracteres)")

        for m in re.finditer(r"\bAnexo\s+(?:N[°º]?\s*)?([A-Z0-9\-]{1,6})\b", texto, re.IGNORECASE):
            anexos_citados.add(f"Anexo {m.group(1).upper()}")

    # Verificar si los anexos citados tienen archivo en bases/
    nombres_archivos_upper = " ".join(p.name.upper() for p in archivos)
    faltantes: list[str] = []
    for anx in sorted(anexos_citados):
        token = anx.split()[-1]
        if token not in nombres_archivos_upper:
            faltantes.append(anx)

    lineas_anexos = [f"- {a}" for a in sorted(anexos_citados)] if anexos_citados else ["- Ninguno detectado automáticamente."]
    lineas_faltantes = (
        [f"- [ ] **{f}** (mencionado en bases pero no se detecta archivo con ese código en `bases/`)" for f in faltantes]
        if faltantes
        else ["- Todos los anexos citados parecen estar presentes en `bases/`."]
    )

    indice_md = [
        f"# Inventario de Bases y Texto Extraído — `{codigo}`",
        "",
        "## Archivos Procesados",
        *(resumen_archivos or ["- (Sin archivos en `bases/`)"]),
        "",
        "## Anexos Mencionados en el Texto de las Bases",
        *lineas_anexos,
        "",
        "## Posibles Anexos Faltantes por Verificar en el Portal",
        *lineas_faltantes,
    ]
    (dest / "bases" / "INVENTARIO_Y_FALTANTES.md").write_text("\n".join(indice_md) + "\n", encoding="utf-8")
    print(f"[OK] Extraídos {len(resumen_archivos)} documento(s) en {out_dir}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Extrae texto de las bases de una licitación.")
    parser.add_argument("codigo", help="Código de la licitación")
    args = parser.parse_args()
    procesar_bases(args.codigo)


if __name__ == "__main__":
    main()
