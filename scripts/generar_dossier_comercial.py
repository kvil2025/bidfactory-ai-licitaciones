"""Genera el Dossier Comercial en Word (`Dossier_Comercial_BidFactory_AI.docx`)
a partir de `README_COMERCIAL_VENTA_B2B.md` e incrusta la infografía de las 50 habilidades,
listo para enviar en PDF/Word a empresas interesadas en adquirir el sistema.
"""
from __future__ import annotations

from pathlib import Path

import docx
from armar_propuesta import agregar_tabla_estilizada, configurar_estilos
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.shared import Cm, Pt, RGBColor

ROOT = Path(__file__).resolve().parent.parent


def generar_dossier_word() -> Path:
    doc = docx.Document()
    configurar_estilos(doc)

    # Portada comercial
    p_tag = doc.add_paragraph()
    r_tag = p_tag.add_run("DOSSIER COMERCIAL Y FICHA TÉCNICA B2B · SOFTWARE & AGENTES IA")
    r_tag.bold = True
    r_tag.font.size = Pt(10)
    r_tag.font.color.rgb = RGBColor(0xEA, 0x58, 0x0C)

    p_tit = doc.add_paragraph()
    p_tit.paragraph_format.space_before = Pt(14)
    r_tit = p_tit.add_run("BidFactory AI — Fábrica de Licitaciones\n50 Habilidades Preconfiguradas para Ingeniería, Minería, Construcción y Energía")
    r_tit.bold = True
    r_tit.font.size = Pt(18)
    r_tit.font.color.rgb = RGBColor(0x0D, 0x25, 0x60)

    p_sub = doc.add_paragraph(
        "Automatización integral del ciclo de propuestas técnicas y económicas: desde que llega el correo de invitación "
        "hasta el Informe del Revisor Final y el Acta del Aprobador de envío."
    )
    p_sub.runs[0].font.size = Pt(11)

    agregar_tabla_estilizada(
        doc,
        ["Atributo del Producto", "Especificación Comercial"],
        [
            ["Arquitectura", "8 Roles Especializados + 50 Habilidades Operativas (SKILL.md) + 9 Motores Python"],
            ["Formatos Automatizados", "Lectura de correos (.eml / Gmail IMAP), bases (.pdf, .docx, .xlsx, .zip) y emisión nativa de Excel (.xlsx) y Word (.docx)"],
            ["Interfaz de Usuario", "Aplicación de Escritorio Windows (.exe) con icono + Panel Web Interactivo"],
            ["Gobierno y Control", "100% Human-in-the-Loop (Go/No-Go, Consultas, Revisión Final y Acta de Aprobación)"],
            [
                "Arquitectura de Datos e IA",
                "Híbrida y Configurable: Archivos y cálculo de costos/precios 100% locales en el PC del cliente + Razonamiento técnico vía API Cloud Empresarial (Gemini / Claude / OpenAI sin entrenamiento de datos) o LLM Local (Ollama).",
            ],
        ],
    )

    img_path = ROOT / "infografia_equipo_licitaciones.png"
    if img_path.exists():
        p_img = doc.add_paragraph()
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img.add_run().add_picture(str(img_path), width=Cm(15.5))

    doc.add_page_break()

    doc.add_heading("1. El Problema que Resuelve en Empresas de Ingeniería y Consultoría", level=1)
    for item in [
        "Reducción de 70% a 80% en las horas de ingeniería senior dedicadas a armar anexos, matrices de cumplimiento, cronogramas y estructura base de propuestas.",
        "Eliminación de errores de inadmisibilidad por omisión de requisitos escondidos en las bases, glosas de garantía o filtración de precios en sobres técnicos.",
        "Coherencia matemática y documental entre lo prometido en la Metodología Técnica, la Carta Gantt, las Horas Hombre (HH) y el Formulario Económico.",
        "Toma de decisión ejecutiva en 10 minutos para el Gerente Técnico / Socio Aprobador mediante el Informe de Revisor Final automatizado con 3 escenarios de precio y margen.",
    ]:
        doc.add_paragraph(item, style="List Bullet")

    doc.add_heading("2. Los 8 Roles del Equipo de Licitaciones IA", level=1)
    agregar_tabla_estilizada(
        doc,
        ["Rol", "Responsabilidad en el Flujo", "Entregable Automático"],
        [
            ["1. Bid Manager", "Orquesta el proceso, plazos y cartera general", "ficha.json, estado.json, cartera_licitaciones.xlsx"],
            ["2. Analista de Bases", "Desglosa BAG, BAE, TdR y detecta anexos faltantes", "matriz_cumplimiento.xlsx + INVENTARIO_Y_FALTANTES.md"],
            ["3. Especialista Técnico", "Redacta capítulos técnicos, Gantt, equipo, HSE y QA/QC", "propuesta_tecnica_<CODIGO>.docx"],
            ["4. Estimador de Costos", "Calcula EDT, HH, gastos directos y 3 escenarios", "costos.xlsx (Agresivo, Objetivo, Conservador)"],
            ["5. Administrativo-Legal", "Verifica garantías, declaraciones juradas y riesgos", "checklist.md, riesgos_contractuales.md"],
            ["6. Revisor QA", "Audita cumplimiento, simula puntaje y verifica formato", "verificacion_estilo_y_formato.md"],
            ["7. Revisor Final (Humano)", "Audita el resumen ejecutivo de calidad, riesgo y margen", "informe_revisor_final.docx"],
            ["8. Aprobador (Humano)", "Autoriza el precio final y firma el pase de envío", "acta_aprobacion.md"],
        ],
    )

    doc.add_heading("3. Arquitectura de Privacidad: Qué es Local y Qué usa LLM en la Nube", level=1)
    agregar_tabla_estilizada(
        doc,
        ["Componente", "Dónde se Ejecuta", "Detalles de Seguridad y Confidencialidad"],
        [
            [
                "Archivos, Tarifas y Cálculo de Costos (costos.xlsx, matriz.xlsx, Word)",
                "100% Local (En el PC o Servidor de la Empresa)",
                "Los scripts Python (.exe) procesan correos .eml, extraen texto de PDFs/ZIPs y calculan las tarifas, márgenes y precios directamente en la CPU local, sin subir las planillas financieras a terceros.",
            ],
            [
                "Opción A: Agentes con LLM Cloud Empresarial (Estándar)",
                "Nube vía API Comercial (Gemini / Claude / OpenAI)",
                "El texto técnico de las bases se analiza con modelos de frontera bajo políticas API Zero-Data-Retention (no se entrenan modelos públicos con la información del cliente).",
            ],
            [
                "Opción B: Modo Híbrido con Costos Aislados",
                "Técnica en Cloud LLM + Económica 100% Local",
                "El LLM redacta el alcance técnico sobre los TdR públicos, pero los precios unitarios, utilidades y el Acta de Aprobación jamás pasan por el LLM.",
            ],
            [
                "Opción C: LLM 100% Local (Air-Gapped)",
                "Servidor GPU interno del Cliente (Ollama / vLLM)",
                "Para clientes mineros o de infraestructura crítica que exigen operación 100% desconectada de internet.",
            ],
        ],
    )

    doc.add_heading("4. Modalidades de Implementación para Empresas Clientes", level=1)
    agregar_tabla_estilizada(
        doc,
        ["Modalidad", "Qué Incluye", "Tiempo de Puesta en Marcha"],
        [
            [
                "Licencia Corporativa Llave en Mano",
                "Instalación completa en PC/servidor del cliente, carga de su Base de Conocimiento (experiencia, equipo, tarifas) y configuración de su plantilla Word corporativa.",
                "24 a 48 horas",
            ],
            [
                "Personalización por Rubro",
                "Adaptación de las 50 habilidades y partidas de costos a la especialidad del cliente (Geotecnia, Minería, Obras Civiles, Montaje Industrial, Energía, Medio Ambiente/SEIA).",
                "1 semana",
            ],
        ],
    )

    out_docx = ROOT / "Dossier_Comercial_BidFactory_AI.docx"
    doc.save(out_docx)
    print(f"[OK] Dossier comercial Word generado en: {out_docx}")
    return out_docx


if __name__ == "__main__":
    generar_dossier_word()
