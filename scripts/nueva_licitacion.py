"""Inicializa la estructura completa de carpetas y archivos para una nueva licitación.

Uso:
    python scripts/nueva_licitacion.py <CODIGO> "<Nombre Licitacion>" "<Mandante>" [--portal "Mercado Público"] [--cierre "YYYY-MM-DD HH:MM"]
"""
from __future__ import annotations

import argparse
import json
import shutil
from datetime import datetime, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LIC_DIR = ROOT / "licitaciones"
TPL_DIR = ROOT / "plantillas"


def calcular_hitos_internos(fecha_cierre_str: str) -> dict[str, str]:
    try:
        dt_cierre = datetime.strptime(fecha_cierre_str[:16], "%Y-%m-%d %H:%M")
    except ValueError:
        try:
            dt_cierre = datetime.strptime(fecha_cierre_str[:10], "%Y-%m-%d")
        except ValueError:
            dt_cierre = datetime.now() + timedelta(days=14)
    return {
        "borrador_tecnico": (dt_cierre - timedelta(days=7)).strftime("%Y-%m-%d"),
        "borrador_economico": (dt_cierre - timedelta(days=5)).strftime("%Y-%m-%d"),
        "revision_qa": (dt_cierre - timedelta(days=4)).strftime("%Y-%m-%d"),
        "revisor_final": (dt_cierre - timedelta(days=2)).strftime("%Y-%m-%d"),
        "aprobacion_envio": (dt_cierre - timedelta(days=1)).strftime("%Y-%m-%d 12:00"),
        "ventana_carga_portal": (dt_cierre - timedelta(days=1)).strftime("%Y-%m-%d 16:00"),
    }


def crear_licitacion(
    codigo: str,
    nombre: str,
    mandante: str,
    portal: str = "Por definir",
    cierre: str | None = None,
) -> Path:
    dest = LIC_DIR / codigo
    subcarpetas = [
        "correo",
        "bases",
        "analisis/texto",
        "consultas",
        "propuesta/secciones",
        "propuesta/figuras",
        "propuesta/cvs",
        "propuesta/economica",
        "propuesta/administrativa",
        "revision",
        "envio",
    ]
    for sub in subcarpetas:
        (dest / sub).mkdir(parents=True, exist_ok=True)

    hoy = datetime.now().strftime("%Y-%m-%d")
    cierre_str = cierre or (datetime.now() + timedelta(days=14)).strftime("%Y-%m-%d 15:00")
    hitos_int = calcular_hitos_internos(cierre_str)

    # 1. ficha.json
    ficha_path = dest / "ficha.json"
    if not ficha_path.exists():
        tpl_ficha = json.loads((TPL_DIR / "ficha_licitacion.json").read_text(encoding="utf-8"))
        tpl_ficha.update(
            {
                "codigo": codigo,
                "nombre": nombre,
                "mandante": mandante,
                "portal": portal,
                "hitos": {
                    "publicacion": hoy,
                    "visita_terreno": "Por confirmar en bases",
                    "cierre_consultas": "Por confirmar en bases",
                    "respuestas_mandante": "Por confirmar en bases",
                    "cierre_ofertas": cierre_str,
                    "apertura_tecnica": cierre_str,
                    "apertura_economica": "Por confirmar en bases",
                    "adjudicacion_estimada": "Por confirmar en bases",
                },
                "hitos_internos": hitos_int,
            }
        )
        ficha_path.write_text(json.dumps(tpl_ficha, indent=2, ensure_ascii=False), encoding="utf-8")

    # 2. estado.json
    estado_path = dest / "estado.json"
    if not estado_path.exists():
        estado = {
            "codigo": codigo,
            "nombre": nombre,
            "mandante": mandante,
            "estado_global": "RECIBIDA",
            "fase_actual": "I - Recepción y triaje",
            "habilidad_actual": 1,
            "urgente": False,
            "go_no_go": {
                "recomendacion_ia": "PENDIENTE",
                "decision_aprobador": "PENDIENTE",
                "aprobado_por": None,
                "fecha": None,
            },
            "consultas": {
                "rondas_enviadas": 0,
                "ultima_actualizacion_matriz": None,
            },
            "revision_final": {
                "estado": "PENDIENTE",
                "revisor": "Carlos Ávila",
                "puntaje_tecnico_simulado": None,
                "observaciones_abiertas": 0,
            },
            "aprobacion": {
                "estado": "PENDIENTE",
                "aprobador": "Carlos Ávila",
                "precio_aprobado": None,
                "moneda": "UF",
                "fecha_hora": None,
            },
            "historial": [
                {
                    "fecha_hora": datetime.now().isoformat(timespec="seconds"),
                    "evento": "Creación de carpeta y estructura inicial de licitación",
                }
            ],
        }
        estado_path.write_text(json.dumps(estado, indent=2, ensure_ascii=False), encoding="utf-8")

    # 3. requisitos.json inicial
    req_path = dest / "analisis" / "requisitos.json"
    if not req_path.exists():
        shutil.copyfile(TPL_DIR / "requisitos_ejemplo.json", req_path)

    # 4. go_no_go.md y checklist.md desde plantillas
    gng_tpl = (TPL_DIR / "go_no_go.md").read_text(encoding="utf-8")
    for k, v in {
        "{{CODIGO}}": codigo,
        "{{NOMBRE}}": nombre,
        "{{MANDANTE}}": mandante,
        "{{CIERRE_OFERTAS}}": cierre_str,
        "{{FECHA_HOY}}": hoy,
    }.items():
        gng_tpl = gng_tpl.replace(k, v)
    (dest / "analisis" / "go_no_go.md").write_text(gng_tpl, encoding="utf-8")

    chk_tpl = (TPL_DIR / "checklist_administrativo.md").read_text(encoding="utf-8").replace("{{CODIGO}}", codigo)
    (dest / "propuesta" / "administrativa" / "checklist.md").write_text(chk_tpl, encoding="utf-8")

    # 5. Secciones base de la propuesta técnica (Habilidades 20 a 27)
    secciones = {
        "01_comprension.md": (
            f"# 1. Comprensión del Problema y Contexto Geológico-Geotécnico\n\n"
            f"## 1.1 Antecedentes Generales de la Licitación `{codigo}`\n"
            f"**Mandante:** {mandante}  \n"
            f"**Proyecto / Servicio:** {nombre}\n\n"
            f"Geologgia Ltda. presenta su propuesta técnica integrando más de 20 años de experiencia de su equipo directivo "
            f"en geología aplicada a la ingeniería, geotecnia, obras subterráneas, minería y energía en Chile.\n\n"
            f"## 1.2 Marco Geológico, Geomorfológico y Geotécnico Local\n"
            f"- Identificación de unidades litológicas, dominios estructurales y condición hidrogeológica del sector.\n"
            f"- Evaluación de singularidades geotécnicas críticas (zonas de falla, alteración, anisotropía y condición de esfuerzos).\n"
        ),
        "02_metodologia.md": (
            "# 2. Metodología de Trabajo y Desarrollo Técnico\n\n"
            "## 2.1 Etapa 1 — Recopilación, Revisión Crítica y Modelo Conceptual Preliminar\n"
            "- Revisión de antecedentes topográficos, geológicos, geofísicos y campañas de sondajes previas.\n"
            "- Fotointerpretación satelital y procesamiento de modelo digital de elevación (DEM ALOS PALSAR 12,5 m / LiDAR).\n\n"
            "## 2.2 Etapa 2 — Levantamiento Geológico-Geotécnico de Terreno y Campaña de Exploración\n"
            "- Mapeo geológico-estructural sistemático y estaciones geomecánicas detalladas (RMR89 de Bieniawski, Q de Barton, GSI de Hoek & Marinos) según normas ISRM.\n"
            "- Supervisión y logueo geotécnico de sondajes (recuperación, RQD, FF, condición de discontinuidades y muestreo para laboratorio según normas ASTM / NCh).\n\n"
            "## 2.3 Etapa 3 — Análisis Geomecánico, Modelamiento y Recomendaciones de Diseño\n"
            "- Definición de Unidades Geotécnicas (UG) y parámetros resistentes equivalentes (Hoek-Brown generalizado / Mohr-Coulomb).\n"
            "- Análisis de estabilidad cinemática, tensional y recomendaciones de soporte / taludes con entrega íntegra en SIG (GeoPackage / Shapefile) y planos CAD.\n"
        ),
        "03_plan_trabajo_equipo.md": (
            "# 3. Plan de Trabajo, Carta Gantt y Organización del Equipo\n\n"
            "## 3.1 Estructura Organizacional y Perfiles Clave\n"
            "El equipo propuesto está liderado directamente por el Socio Director de Geologgia Ltda., asegurando presencia senior en terreno y en las reuniones de coordinación con el Mandante.\n\n"
            "## 3.2 Secuencia Constructiva del Estudio y Control de Plazos\n"
            "La Carta Gantt adjunta detalla las actividades semanales, hitos de entrega parcial y revisiones conjuntas con la contraparte técnica del Mandante.\n"
        ),
        "04_hse.md": (
            "# 4. Plan de Seguridad, Salud Ocupacional y Medio Ambiente (HSE / SSOMA)\n\n"
            "## 4.1 Identificación de Peligros y Control de Riesgos Críticos en Terreno\n"
            "- Cumplimiento estricto del DS N° 132 (Reglamento de Seguridad Minera), DS N° 594 y Reglamento Especial de Empresas Contratistas (REECC) del Mandante.\n"
            "- Controles específicos para conducción 4x4 en caminos de faena, trabajo en taludes y caída de rocas, exposición a altura geográfica (hipobaria intermitente crónica) y operación cercana a equipos de perforación.\n"
        ),
        "05_calidad.md": (
            "# 5. Aseguramiento y Control de Calidad (QA/QC) y Entregables\n\n"
            "## 5.1 Trazabilidad de Datos de Terreno y Gabinete\n"
            "- Doble control cruzado (Revisión Par Senior) de libretas de mapeo, planillas de logueo geotécnico, bases de datos SIG y memoria de cálculo antes de cada emisión (Revisión B y Revisión 0).\n"
        ),
    }
    for fname, content in secciones.items():
        p = dest / "propuesta" / "secciones" / fname
        if not p.exists():
            p.write_text(content, encoding="utf-8")

    # 6. gantt.csv y equipo.csv iniciales
    gantt_csv = dest / "propuesta" / "gantt.csv"
    if not gantt_csv.exists():
        gantt_csv.write_text(
            "id,actividad,semana_inicio,duracion_semanas,responsable,entregable\n"
            "1,Reunión de inicio (Kick-off) y recopilación de antecedentes,1,1,Jefe de Proyecto,Minuta Kick-off y Plan de Terreno\n"
            "2,Campaña de levantamiento geológico-geotécnico y supervisión en terreno,2,4,Jefe de Terreno + Geólogos,Informe de Terreno y Base de Datos Preliminar\n"
            "3,Ensayos de laboratorio y procesamiento geomecánico / SIG,5,3,Especialista Geotécnico + GIS,Base Georreferenciada y Parámetros UG\n"
            "4,Modelamiento geotécnico e Informe Borrador (Rev. B),7,2,Director de Proyecto,Informe Técnico Rev. B\n"
            "5,Levantamiento de observaciones del Mandante e Informe Final (Rev. 0),9,1,Director de Proyecto,Informe Final Rev. 0 + Planos + GIS\n",
            encoding="utf-8",
        )

    equipo_csv = dest / "propuesta" / "equipo.csv"
    if not equipo_csv.exists():
        equipo_csv.write_text(
            "rol,nombre,profesion,anos_experiencia,dedicacion_pct,experiencia_destacada\n"
            "Director / Jefe de Proyecto,Carlos Cristian Ávila Elgueta,Geólogo,22,50%,7 centrales hidroeléctricas (~80 km túneles) y ~20 km túneles mineros Codelco\n"
            "Geólogo Geotécnico Senior,Especialista Senior Asociado,Geólogo / Ing. Civil,14,75%,Mapeo geomecánico RMR/Q/GSI y supervisión de campañas de sondajes\n"
            "Geólogo de Terreno,Geólogo de Campo Geologgia,Geólogo,6,100%,Levantamiento estructural y logueo geotécnico en faena\n"
            "Especialista GIS y Modelamiento 3D,Especialista Geomática Geologgia,Ing. Geomensor / Geólogo GIS,7,50%,Cartografía SERNAGEOMIN / DEM ALOS PALSAR / modelos 3D\n"
            "Asesor HSE / APR,Prevencionista Asociado,Ing. Prevención de Riesgos,8,25%,Acreditación minera DS132 / REECC y control de riesgos en terreno\n",
            encoding="utf-8",
        )

    print(f"[OK] Licitación '{codigo}' creada en: {dest}")
    return dest


def main() -> None:
    parser = argparse.ArgumentParser(description="Crea la estructura de una nueva licitación.")
    parser.add_argument("codigo", help="Código único de la licitación (ej. LIC-2026-001)")
    parser.add_argument("nombre", help="Nombre oficial de la licitación")
    parser.add_argument("mandante", help="Nombre del mandante o cliente")
    parser.add_argument("--portal", default="Por definir", help="Canal o portal (Mercado Público, SAP Ariba, Correo)")
    parser.add_argument("--cierre", default=None, help="Fecha y hora de cierre (YYYY-MM-DD HH:MM)")
    args = parser.parse_args()
    crear_licitacion(args.codigo, args.nombre, args.mandante, args.portal, args.cierre)


if __name__ == "__main__":
    main()
