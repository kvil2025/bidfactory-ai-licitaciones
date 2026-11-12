"""Genera la aplicación web estática lista para Vercel (`web/index.html` + logos en `web/`)
y sincroniza `panel_equipo_licitaciones.html` con:
- Diseño Apple HIG Pro (SF Pro / Inter, monocromático sobrio, superficies traslúcidas con blur, bordes finos 1px, sin colores chillones).
- Selector instantáneo de Modo Claro (Light) y Modo Oscuro (Dark) con persistencia.
- Branding conjunto oficial: "Desarrollado por Tecknologia" (`logo-tecknologia.png`) y "Diseñado por Geologgia Ltda." (`logo-geologgia.png`).
- 4 Licitaciones de Demostración Ficticias (100% inventadas para la demo comercial en Vercel, sin exponer correos ni clientes reales confidenciales):
  1. DEMO-MIN-2026: Estudio Geotécnico e Hidrogeológico Caverna de Chancado Subterráneo — Compañía Minera Cumbre Andina S.A.
  2. DEMO-ENE-2026: Evaluación de Peligros Geológicos y Cambio Climático Central Hidroeléctrica Río Blanco — Austral Generación SpA
  3. DEMO-INF-2026: Ingeniería Geológica de Detalle y Soporte NATM Túnel Vial Cordillera — Concesionaria Vial del Sur S.A.
  4. DEMO-CLM-2026: Peritaje Geotécnico y Línea Base (GBR) por Condición de Terreno Imprevista — Constructora Túneles del Pacífico Ltda.
"""
from __future__ import annotations

import json
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(r"C:\Users\geolo\.gemini\antigravity\brain\62ed66f6-4ba4-4c5f-b03f-e01bcc1f2f58\scratch")))
from generar_habilidades import FASES, H  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
WEB_DIR = ROOT / "web"
ASSETS_DIR = ROOT / "assets"
BRAND_LOGOS = Path(r"C:\Users\geolo\.gemini\config\skills\brand-assets\logos")


LICITACIONES_DEMO_FICTICIAS = [
    {
        "codigo": "DEMO-MIN-2026",
        "nombre": "Estudio Geotécnico e Hidrogeológico para Caverna de Chancado Subterráneo y Piques de Ventilación",
        "mandante": "Compañía Minera Cumbre Andina S.A. (Ejemplo Demo)",
        "portal": "SAP Ariba Enterprise",
        "modalidad": "Suma Alzada en UF (Dos Sobres)",
        "ubicacion": "Faena Alta Cordillera, Región de Antofagasta (3.850 m s.n.m.)",
        "cierre": "2026-12-04 15:00",
        "estado_global": "APROBADA PARA ENVÍO",
        "go_no_go_nota": "4.75 / 5.00 (GO)",
        "puntaje_simulado": 96.8,
        "cumplimiento_pct": 100,
        "inadmisibilidad_pendientes": 0,
        "plazo_semanas": 12,
        "hh_totales": 620,
        "escenarios": {
            "costo_directo": 1140.00,
            "agresivo": 1468.32,
            "objetivo": 1587.34,
            "conservador": 1738.50,
            "aprobado": 1580.00,
        },
        "revisor_final": "Director Técnico / Socio Aprobador",
        "requisitos": [
            {"id": "ADM-001", "cat": "Administrativo", "req": "Boleta de Garantía de Seriedad por 300 UF vigencia 90 días", "fuente": "BAG Numeral 8.1", "inadm": True, "estado": "Cumple"},
            {"id": "ADM-002", "cat": "Administrativo", "req": "Certificado F30 y Declaración Ley 20.393 firmada", "fuente": "BAG Anexo A-2", "inadm": True, "estado": "Cumple"},
            {"id": "TEC-001", "cat": "Técnico", "req": "Logueo geotécnico de 800 m de sondajes orientados HQ3 y caracterización RMR89, Q y GSI", "fuente": "TdR Cap. 4.2", "inadm": True, "estado": "Cumple"},
            {"id": "TEC-002", "cat": "Técnico", "req": "Modelamiento numérico tridimensional de esfuerzos y fortificación de caverna", "fuente": "TdR Cap. 4.5", "inadm": True, "estado": "Cumple"},
            {"id": "EXP-001", "cat": "Experiencia", "req": "Jefe de Proyecto con +15 años en obras subterráneas mineras o hidroeléctricas", "fuente": "BAE Numeral 5.3", "inadm": True, "estado": "Cumple"},
            {"id": "ECO-001", "cat": "Económico", "req": "Formulario Económico E-1 desglosado por partida sin filtración en sobre técnico", "fuente": "BAE Anexo E-1", "inadm": True, "estado": "Cumple"},
        ],
    },
    {
        "codigo": "DEMO-ENE-2026",
        "nombre": "Actualización de Estudio de Peligros Geológicos y Forzante de Cambio Climático en Central Hidroeléctrica",
        "mandante": "Austral Generación Renovable SpA (Ejemplo Demo)",
        "portal": "Invitación Directa + Data Room",
        "modalidad": "Suma Alzada por Hitos",
        "ubicacion": "Cuenca Cordillerana Zona Central, Chile (1.900 m s.n.m.)",
        "cierre": "2026-11-28 18:00",
        "estado_global": "EN REVISIÓN FINAL (HAB. 47)",
        "go_no_go_nota": "4.80 / 5.00 (GO)",
        "puntaje_simulado": 96.5,
        "cumplimiento_pct": 100,
        "inadmisibilidad_pendientes": 0,
        "plazo_semanas": 10,
        "hh_totales": 442,
        "escenarios": {
            "costo_directo": 812.75,
            "agresivo": 1046.82,
            "objetivo": 1131.67,
            "conservador": 1239.44,
            "aprobado": 1130.00,
        },
        "revisor_final": "Director Técnico / Socio Aprobador",
        "requisitos": [
            {"id": "TEC-001", "cat": "Técnico", "req": "Alcance detallado en 5 etapas incluyendo campaña geomorfológica en terreno", "fuente": "Solicitud RFQ Párr. 2", "inadm": True, "estado": "Cumple"},
            {"id": "TEC-002", "cat": "Técnico", "req": "Modelación de ascenso de isoterma 0°C y lluvias extremas (ARCliM / CMIP6)", "fuente": "Solicitud RFQ Párr. 1", "inadm": True, "estado": "Cumple"},
            {"id": "TEC-003", "cat": "Técnico", "req": "Atlas de Peligro (Escenario Histórico vs Cambio Climático) y Geodatabase SIG (.gpkg)", "fuente": "Solicitud RFQ Párr. 2", "inadm": True, "estado": "Cumple"},
            {"id": "TEC-004", "cat": "Técnico", "req": "Fichas operacionales de vulnerabilidad y riesgo por activo (bocatoma, canal, casa de máquinas)", "fuente": "TdR Sección 5", "inadm": False, "estado": "Cumple"},
            {"id": "ECO-001", "cat": "Económico", "req": "Cuadro económico en UF y supuestos operacionales de acceso", "fuente": "Solicitud RFQ Párr. 2", "inadm": True, "estado": "Cumple"},
        ],
    },
    {
        "codigo": "DEMO-INF-2026",
        "nombre": "Ingeniería Geológica-Geotécnica de Detalle para Portales y Soporte NATM de Túnel Vial (3,6 km)",
        "mandante": "Sociedad Concesionaria Vial Cordillera S.A. (Ejemplo Demo)",
        "portal": "Mercado Público / MOP",
        "modalidad": "Serie de Precios Unitarios + Suma Alzada",
        "ubicacion": "Tramo Cordillerano Ruta Internacional, Región del Maule",
        "cierre": "2026-12-15 12:00",
        "estado_global": "EN PREPARACIÓN TÉCNICA (FASE IV)",
        "go_no_go_nota": "4.35 / 5.00 (GO)",
        "puntaje_simulado": 93.0,
        "cumplimiento_pct": 88,
        "inadmisibilidad_pendientes": 1,
        "plazo_semanas": 16,
        "hh_totales": 780,
        "escenarios": {
            "costo_directo": 1490.00,
            "agresivo": 1919.12,
            "objetivo": 2074.68,
            "conservador": 2272.25,
            "aprobado": None,
        },
        "revisor_final": "Director Técnico / Socio Aprobador",
        "requisitos": [
            {"id": "ADM-001", "cat": "Administrativo", "req": "Certificado vigente en Registro de Consultores MOP Área Geología y Mecánica de Rocas", "fuente": "BAG Numeral 4.2", "inadm": True, "estado": "Cumple"},
            {"id": "ADM-002", "cat": "Administrativo", "req": "Garantía de Seriedad de la Oferta por 450 UF", "fuente": "BAG Numeral 9.1", "inadm": True, "estado": "En curso"},
            {"id": "TEC-001", "cat": "Técnico", "req": "Mapeo geomecánico de portales y perfiles de refracción sísmica / MASW", "fuente": "TdR Cap. 3", "inadm": True, "estado": "Cumple"},
            {"id": "TEC-002", "cat": "Técnico", "req": "Diseño de clases de excavación y soporte primario NATM según estándar Manual de Carreteras Vol. 3", "fuente": "TdR Cap. 5", "inadm": True, "estado": "Cumple"},
        ],
    },
    {
        "codigo": "DEMO-CLM-2026",
        "nombre": "Informe Pericial Geotécnico por Condición de Terreno Imprevista (Differing Site Conditions) en Túnel de Aducción",
        "mandante": "Constructora Obras Subterráneas del Pacífico Ltda. (Ejemplo Demo)",
        "portal": "Invitación Directa Confidencial (NDA)",
        "modalidad": "Tarifas HH + Suma Alzada Informe Pericial",
        "ubicacion": "Región del Biobío, Chile",
        "cierre": "2026-11-25 18:00",
        "estado_global": "APROBADA PARA ENVÍO",
        "go_no_go_nota": "4.90 / 5.00 (GO)",
        "puntaje_simulado": 99.0,
        "cumplimiento_pct": 100,
        "inadmisibilidad_pendientes": 0,
        "plazo_semanas": 6,
        "hh_totales": 310,
        "escenarios": {
            "costo_directo": 645.00,
            "agresivo": 830.76,
            "objetivo": 898.10,
            "conservador": 983.63,
            "aprobado": 980.00,
        },
        "revisor_final": "Director Técnico / Socio Aprobador",
        "requisitos": [
            {"id": "TEC-001", "cat": "Técnico", "req": "Contraste entre Informe Geotécnico de Línea Base (GBR) de licitación y mapeo real de frentes ejecutados", "fuente": "TdR Peritaje Numeral 2.1", "inadm": True, "estado": "Cumple"},
            {"id": "TEC-002", "cat": "Técnico", "req": "Cuantificación de impacto en rendimientos de avance y sobre-soporte por zona de falla no prevista", "fuente": "TdR Peritaje Numeral 2.3", "inadm": True, "estado": "Cumple"},
            {"id": "EXP-001", "cat": "Experiencia", "req": "Perito Geólogo Senior con +20 años en túneles y experiencia en paneles técnicos / arbitrajes", "fuente": "TdR Peritaje Numeral 3.1", "inadm": True, "estado": "Cumple"},
        ],
    },
]


def copiar_logos() -> None:
    for target_dir in [WEB_DIR, ASSETS_DIR]:
        target_dir.mkdir(parents=True, exist_ok=True)
        for logo_name in ["logo-tecknologia.png", "logo-geologgia.png"]:
            src = BRAND_LOGOS / logo_name
            if src.exists():
                shutil.copy2(src, target_dir / logo_name)


def generar_html_apple_hig() -> None:
    copiar_logos()

    fases_list = [
        {"id": k, "carpeta": v[0], "titulo": v[1]}
        for k, v in FASES.items()
    ]
    skills_json = json.dumps(H, ensure_ascii=False)
    fases_json = json.dumps(fases_list, ensure_ascii=False)
    demos_json = json.dumps(LICITACIONES_DEMO_FICTICIAS, ensure_ascii=False)

    html = f"""<!DOCTYPE html>
<html lang="es" data-theme="dark">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<title>BidFactory AI — Equipo de Licitaciones | Desarrollado por Tecknologia · Diseñado por Geologgia Ltda.</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
<style>
  /* ==========================================================================
     APPLE HUMAN INTERFACE GUIDELINES (HIG) — LIGHT & DARK MODE TOKENS
     Diseño sobrio, monocromático de alto contraste, tipografía SF Pro / Inter,
     superficies traslúcidas (vibrancy) y un solo acento azul de sistema.
     ========================================================================== */
  :root[data-theme="light"] {{
    --bg-primary: #F5F5F7;
    --bg-secondary: #FFFFFF;
    --bg-tertiary: #FAFAFC;
    --bg-elevated: rgba(255, 255, 255, 0.82);
    --bg-pill: #EFEFF4;
    --bg-hover: rgba(0, 0, 0, 0.04);
    --label-primary: #1D1D1F;
    --label-secondary: #515154;
    --label-tertiary: #86868B;
    --separator: rgba(0, 0, 0, 0.09);
    --separator-strong: rgba(0, 0, 0, 0.16);
    --accent: #0066CC;
    --accent-soft: rgba(0, 102, 204, 0.10);
    --status-ok: #1D7D3F;
    --status-ok-bg: rgba(29, 125, 63, 0.10);
    --status-warn: #B25000;
    --status-warn-bg: rgba(178, 80, 0, 0.10);
    --num-bg: #F2F2F7;
    --num-text: #1D1D1F;
    --shadow-card: 0 2px 12px rgba(0, 0, 0, 0.04), 0 1px 2px rgba(0, 0, 0, 0.03);
    --shadow-modal: 0 24px 60px rgba(0, 0, 0, 0.18);
    --teck-logo-bg: #1D1D1F;
  }}

  :root[data-theme="dark"] {{
    --bg-primary: #000000;
    --bg-secondary: #121214;
    --bg-tertiary: #1C1C1E;
    --bg-elevated: rgba(28, 28, 30, 0.78);
    --bg-pill: #2C2C2E;
    --bg-hover: rgba(255, 255, 255, 0.05);
    --label-primary: #F5F5F7;
    --label-secondary: #A1A1A6;
    --label-tertiary: #6E6E73;
    --separator: rgba(255, 255, 255, 0.10);
    --separator-strong: rgba(255, 255, 255, 0.18);
    --accent: #0A84FF;
    --accent-soft: rgba(10, 132, 255, 0.14);
    --status-ok: #30D158;
    --status-ok-bg: rgba(48, 209, 88, 0.14);
    --status-warn: #FF9F0A;
    --status-warn-bg: rgba(255, 159, 10, 0.14);
    --num-bg: #242426;
    --num-text: #E5E5EA;
    --shadow-card: 0 4px 20px rgba(0, 0, 0, 0.45);
    --shadow-modal: 0 28px 70px rgba(0, 0, 0, 0.75);
    --teck-logo-bg: transparent;
  }}

  * {{
    box-sizing: border-box;
    margin: 0;
    padding: 0;
  }}

  body {{
    font-family: -apple-system, BlinkMacSystemFont, "SF Pro Display", "SF Pro Text", "Inter", "Helvetica Neue", Arial, sans-serif;
    background-color: var(--bg-primary);
    color: var(--label-primary);
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    min-height: 100vh;
    display: flex;
    flex-direction: column;
    transition: background-color 0.25s ease, color 0.25s ease;
  }}

  /* Barra de Navegación Superior Translúcida (Apple Frosted Glass) */
  .apple-navbar {{
    position: sticky;
    top: 0;
    z-index: 40;
    background: var(--bg-elevated);
    backdrop-filter: saturate(180%) blur(20px);
    -webkit-backdrop-filter: saturate(180%) blur(20px);
    border-bottom: 1px solid var(--separator);
    padding: 10px 24px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 16px;
  }}

  .brand-cluster {{
    display: flex;
    align-items: center;
    gap: 18px;
    flex-wrap: wrap;
  }}

  .brand-item {{
    display: flex;
    align-items: center;
    gap: 8px;
  }}

  .brand-caption {{
    font-size: 11px;
    font-weight: 500;
    color: var(--label-tertiary);
    letter-spacing: 0.01em;
  }}

  .logo-teck {{
    height: 28px;
    width: auto;
    background: var(--teck-logo-bg);
    padding: 3px 8px;
    border-radius: 6px;
    object-fit: contain;
  }}

  .logo-geologgia {{
    height: 28px;
    width: auto;
    background: #FFFFFF;
    padding: 3px 8px;
    border-radius: 6px;
    border: 1px solid rgba(0, 0, 0, 0.08);
    object-fit: contain;
  }}

  .brand-divider {{
    width: 1px;
    height: 22px;
    background: var(--separator-strong);
  }}

  /* Segmented Control (Pestañas estilo macOS / iPadOS) */
  .segmented-control {{
    display: inline-flex;
    background: var(--bg-pill);
    padding: 3px;
    border-radius: 10px;
    border: 1px solid var(--separator);
  }}

  .seg-btn {{
    border: none;
    background: transparent;
    color: var(--label-secondary);
    font-size: 13px;
    font-weight: 500;
    padding: 6px 14px;
    border-radius: 7px;
    cursor: pointer;
    transition: all 0.18s ease;
    font-family: inherit;
  }}

  .seg-btn.active {{
    background: var(--bg-secondary);
    color: var(--label-primary);
    font-weight: 600;
    box-shadow: 0 1px 4px rgba(0, 0, 0, 0.12);
  }}

  /* Botón de cambio de tema Light / Dark */
  .theme-toggle {{
    display: inline-flex;
    align-items: center;
    gap: 7px;
    background: var(--bg-secondary);
    color: var(--label-primary);
    border: 1px solid var(--separator-strong);
    padding: 6px 13px;
    border-radius: 999px;
    font-size: 12.5px;
    font-weight: 500;
    cursor: pointer;
    font-family: inherit;
    transition: all 0.18s ease;
  }}

  .theme-toggle:hover {{
    border-color: var(--accent);
  }}

  /* Layout Principal */
  .layout-shell {{
    display: grid;
    grid-template-columns: 260px 1fr;
    flex: 1;
    max-width: 1640px;
    width: 100%;
    margin: 0 auto;
  }}

  @media (max-width: 1024px) {{
    .layout-shell {{
      grid-template-columns: 1fr;
    }}
    .sidebar {{
      display: none;
    }}
  }}

  /* Sidebar estilo macOS Finder */
  .sidebar {{
    border-right: 1px solid var(--separator);
    padding: 20px 12px;
    background: var(--bg-primary);
    overflow-y: auto;
    max-height: calc(100vh - 57px);
    position: sticky;
    top: 57px;
  }}

  .sidebar-section-label {{
    font-size: 11px;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    color: var(--label-tertiary);
    padding: 6px 10px;
  }}

  .tree-group {{
    margin-bottom: 6px;
  }}

  .tree-folder {{
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 6px 10px;
    border-radius: 7px;
    font-size: 12.5px;
    font-weight: 600;
    color: var(--label-primary);
    cursor: pointer;
    transition: background 0.15s;
  }}

  .tree-folder:hover {{
    background: var(--bg-hover);
  }}

  .folder-badge {{
    font-size: 11px;
    color: var(--label-tertiary);
    font-variant-numeric: tabular-nums;
  }}

  .tree-children {{
    padding-left: 12px;
    margin-top: 2px;
  }}

  .tree-leaf {{
    padding: 4px 10px;
    border-radius: 6px;
    font-size: 12px;
    color: var(--label-secondary);
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: space-between;
    font-variant-numeric: tabular-nums;
  }}

  .tree-leaf:hover {{
    background: var(--bg-hover);
    color: var(--label-primary);
  }}

  /* Contenedor Central */
  .content-area {{
    padding: 32px 36px 48px;
  }}

  .hero-header {{
    display: flex;
    justify-content: space-between;
    align-items: flex-end;
    gap: 24px;
    padding-bottom: 24px;
    border-bottom: 1px solid var(--separator);
    margin-bottom: 28px;
    flex-wrap: wrap;
  }}

  .eyebrow {{
    font-size: 12px;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    color: var(--accent);
    margin-bottom: 6px;
  }}

  .hero-title {{
    font-size: 34px;
    font-weight: 700;
    letter-spacing: -0.025em;
    line-height: 1.12;
    color: var(--label-primary);
  }}

  .hero-subtitle {{
    margin-top: 8px;
    font-size: 15px;
    line-height: 1.5;
    color: var(--label-secondary);
    max-width: 720px;
  }}

  .roles-strip {{
    display: flex;
    gap: 6px;
    flex-wrap: wrap;
  }}

  .role-chip {{
    font-size: 12px;
    font-weight: 500;
    padding: 5px 11px;
    border-radius: 999px;
    background: var(--bg-secondary);
    border: 1px solid var(--separator);
    color: var(--label-secondary);
  }}

  .role-chip.primary {{
    color: var(--accent);
    border-color: var(--accent);
    background: var(--accent-soft);
    font-weight: 600;
  }}

  /* Grid 2x4 de las 8 Fases (Apple Cards limpias, sin colores estridentes) */
  .phases-grid {{
    display: grid;
    grid-template-columns: repeat(2, minmax(340px, 1fr));
    gap: 18px;
  }}

  @media (max-width: 900px) {{
    .phases-grid {{
      grid-template-columns: 1fr;
    }}
  }}

  .phase-card {{
    background: var(--bg-secondary);
    border: 1px solid var(--separator);
    border-radius: 14px;
    padding: 18px 20px;
    box-shadow: var(--shadow-card);
    transition: border-color 0.2s ease, transform 0.2s ease;
  }}

  .phase-card:hover {{
    border-color: var(--separator-strong);
  }}

  .phase-card-header {{
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding-bottom: 12px;
    margin-bottom: 10px;
    border-bottom: 1px solid var(--separator);
  }}

  .phase-card-title {{
    font-size: 16px;
    font-weight: 600;
    letter-spacing: -0.01em;
    color: var(--label-primary);
  }}

  .phase-range-pill {{
    font-size: 11.5px;
    font-weight: 500;
    color: var(--label-tertiary);
    background: var(--bg-pill);
    padding: 3px 9px;
    border-radius: 999px;
  }}

  .skill-item {{
    display: flex;
    align-items: center;
    gap: 11px;
    padding: 6px 8px;
    border-radius: 8px;
    cursor: pointer;
    transition: background 0.14s ease;
  }}

  .skill-item:hover {{
    background: var(--bg-hover);
  }}

  .skill-index {{
    font-size: 11.5px;
    font-weight: 600;
    font-variant-numeric: tabular-nums;
    background: var(--num-bg);
    color: var(--num-text);
    padding: 2px 7px;
    border-radius: 6px;
    min-width: 28px;
    text-align: center;
    border: 1px solid var(--separator);
  }}

  .skill-label {{
    font-size: 13.5px;
    color: var(--label-primary);
    flex: 1;
  }}

  .gate-pill {{
    font-size: 10.5px;
    font-weight: 600;
    color: var(--accent);
    background: var(--accent-soft);
    padding: 2px 7px;
    border-radius: 999px;
  }}

  /* Simulador / Demo Interactiva de Licitaciones Ficticias */
  .demo-layout {{
    display: grid;
    grid-template-columns: 310px 1fr;
    gap: 20px;
  }}

  @media (max-width: 960px) {{
    .demo-layout {{
      grid-template-columns: 1fr;
    }}
  }}

  .demo-selector-card {{
    background: var(--bg-secondary);
    border: 1px solid var(--separator);
    border-radius: 14px;
    padding: 16px;
    box-shadow: var(--shadow-card);
    height: fit-content;
  }}

  .demo-item {{
    padding: 12px;
    border-radius: 10px;
    border: 1px solid transparent;
    cursor: pointer;
    margin-bottom: 8px;
    transition: all 0.16s ease;
  }}

  .demo-item:hover {{
    background: var(--bg-hover);
  }}

  .demo-item.active {{
    background: var(--accent-soft);
    border-color: var(--accent);
  }}

  .demo-code {{
    font-size: 11.5px;
    font-weight: 700;
    color: var(--accent);
    letter-spacing: 0.02em;
  }}

  .demo-name {{
    font-size: 13px;
    font-weight: 600;
    color: var(--label-primary);
    margin-top: 3px;
    line-height: 1.35;
  }}

  .demo-client {{
    font-size: 11.5px;
    color: var(--label-secondary);
    margin-top: 3px;
  }}

  .kpi-grid {{
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 12px;
    margin-bottom: 18px;
  }}

  @media (max-width: 780px) {{
    .kpi-grid {{
      grid-template-columns: repeat(2, 1fr);
    }}
  }}

  .kpi-box {{
    background: var(--bg-secondary);
    border: 1px solid var(--separator);
    border-radius: 12px;
    padding: 14px 16px;
    box-shadow: var(--shadow-card);
  }}

  .kpi-title {{
    font-size: 11.5px;
    color: var(--label-tertiary);
    font-weight: 500;
  }}

  .kpi-number {{
    font-size: 22px;
    font-weight: 700;
    color: var(--label-primary);
    margin-top: 4px;
    letter-spacing: -0.02em;
    font-variant-numeric: tabular-nums;
  }}

  .kpi-foot {{
    font-size: 11.5px;
    color: var(--label-secondary);
    margin-top: 3px;
  }}

  .apple-table-wrap {{
    background: var(--bg-secondary);
    border: 1px solid var(--separator);
    border-radius: 14px;
    padding: 18px 20px;
    box-shadow: var(--shadow-card);
    margin-bottom: 18px;
    overflow-x: auto;
  }}

  table.apple-table {{
    width: 100%;
    border-collapse: collapse;
    font-size: 13px;
  }}

  table.apple-table th {{
    text-align: left;
    font-size: 11px;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.04em;
    color: var(--label-tertiary);
    padding: 10px 12px;
    border-bottom: 1px solid var(--separator-strong);
  }}

  table.apple-table td {{
    padding: 11px 12px;
    border-bottom: 1px solid var(--separator);
    color: var(--label-primary);
    vertical-align: top;
  }}

  table.apple-table tr:last-child td {{
    border-bottom: none;
  }}

  .badge-status {{
    display: inline-block;
    font-size: 11px;
    font-weight: 600;
    padding: 3px 9px;
    border-radius: 999px;
  }}

  .badge-status.ok {{
    color: var(--status-ok);
    background: var(--status-ok-bg);
  }}

  .badge-status.warn {{
    color: var(--status-warn);
    background: var(--status-warn-bg);
  }}

  .btn-primary-apple {{
    background: var(--accent);
    color: #FFFFFF;
    border: none;
    padding: 8px 16px;
    border-radius: 999px;
    font-size: 13px;
    font-weight: 600;
    cursor: pointer;
    font-family: inherit;
    transition: opacity 0.15s;
  }}

  .btn-primary-apple:hover {{
    opacity: 0.9;
  }}

  /* Modal Estilo macOS Sheet */
  .modal-backdrop {{
    position: fixed;
    inset: 0;
    background: rgba(0, 0, 0, 0.48);
    backdrop-filter: blur(8px);
    -webkit-backdrop-filter: blur(8px);
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 60;
    padding: 20px;
  }}

  .modal-sheet {{
    background: var(--bg-secondary);
    border: 1px solid var(--separator-strong);
    border-radius: 16px;
    width: min(660px, 95vw);
    padding: 26px 28px;
    box-shadow: var(--shadow-modal);
  }}

  .modal-sheet h2 {{
    font-size: 20px;
    font-weight: 700;
    color: var(--label-primary);
  }}

  .modal-meta {{
    font-size: 12.5px;
    color: var(--label-secondary);
    margin-top: 4px;
    padding-bottom: 14px;
    border-bottom: 1px solid var(--separator);
  }}

  .modal-section-title {{
    font-size: 11px;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    color: var(--label-tertiary);
    margin: 14px 0 6px;
  }}

  .modal-sheet ul, .modal-sheet ol {{
    padding-left: 18px;
    font-size: 13.5px;
    line-height: 1.55;
    color: var(--label-primary);
  }}

  .close-pill {{
    float: right;
    background: var(--bg-pill);
    border: 1px solid var(--separator);
    color: var(--label-primary);
    padding: 5px 12px;
    border-radius: 999px;
    font-size: 12px;
    font-weight: 500;
    cursor: pointer;
  }}

  /* Footer Corporativo Oficial */
  .apple-footer {{
    border-top: 1px solid var(--separator);
    background: var(--bg-secondary);
    padding: 20px 36px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    flex-wrap: wrap;
    gap: 16px;
    font-size: 12px;
    color: var(--label-tertiary);
  }}

  .hidden {{
    display: none !important;
  }}
</style>
</head>
<body>

<!-- Barra Superior Translúcida con Logos Oficiales y Controles -->
<header class="apple-navbar">
  <div class="brand-cluster">
    <div class="brand-item">
      <span class="brand-caption">Desarrollado por</span>
      <img src="logo-tecknologia.png" alt="Tecknologia" class="logo-teck" />
    </div>
    <div class="brand-divider"></div>
    <div class="brand-item">
      <span class="brand-caption">Diseñado por</span>
      <img src="logo-geologgia.png" alt="Geologgia Ltda." class="logo-geologgia" />
    </div>
  </div>

  <nav class="segmented-control" aria-label="Vistas principales">
    <button class="seg-btn active" id="tab-mapa" onclick="switchView('mapa')">50 Habilidades</button>
    <button class="seg-btn" id="tab-demo" onclick="switchView('demo')">Simulador & Cartera Demo (4)</button>
    <button class="seg-btn" id="tab-arquitectura" onclick="switchView('arquitectura')">Arquitectura & Privacidad</button>
  </nav>

  <button class="theme-toggle" onclick="toggleTheme()" id="theme-btn" title="Cambiar entre modo claro y oscuro">
    <span id="theme-icon">☀️</span>
    <span id="theme-label">Modo Claro</span>
  </button>
</header>

<div class="layout-shell">
  <!-- Barra Lateral de Exploración de las 50 Skills -->
  <aside class="sidebar">
    <div class="sidebar-section-label">Estructura · 50 Habilidades</div>
    <div id="sidebar-tree"></div>
  </aside>

  <!-- Área Principal -->
  <main class="content-area">
    <!-- VISTA 1: LAS 50 HABILIDADES EN 8 FASES -->
    <section id="view-mapa">
      <div class="hero-header">
        <div>
          <div class="eyebrow">Ingeniería de Propuestas Asistida por IA</div>
          <h1 class="hero-title">Equipo de Licitaciones</h1>
          <p class="hero-subtitle">
            50 habilidades preconfiguradas y auditables para organizar, costear y controlar todo el ciclo de licitaciones en Geología, Geotecnia, Minería, Construcción y Energía — desde el correo de invitación hasta la firma del Aprobador.
          </p>
        </div>
        <div class="roles-strip">
          <span class="role-chip">01 · Bid Manager</span>
          <span class="role-chip">02 · Analista de Bases</span>
          <span class="role-chip">03 · Especialista Técnico</span>
          <span class="role-chip">04 · Estimador de Costos</span>
          <span class="role-chip">05 · Administrativo-Legal</span>
          <span class="role-chip">06 · Revisor QA</span>
          <span class="role-chip primary">07 & 08 · Revisor Final y Aprobador</span>
        </div>
      </div>

      <div class="phases-grid" id="phases-container"></div>
    </section>

    <!-- VISTA 2: SIMULADOR INTERACTIVO CON 4 LICITACIONES FICTICIAS DE DEMOSTRACIÓN -->
    <section id="view-demo" class="hidden">
      <div class="hero-header">
        <div>
          <div class="eyebrow">Entorno de Demostración Interactiva (Datos Ficticios)</div>
          <h1 class="hero-title">Consola de Cartera y Aprobación</h1>
          <p class="hero-subtitle">
            Explora 4 casos simulados de minería subterránea, hidroelectricidad, infraestructura vial y reclamos contractuales (*claims*). Prueba la aprobación de precio en vivo como Revisor Final.
          </p>
        </div>
      </div>

      <div class="demo-layout">
        <div class="demo-selector-card">
          <div class="sidebar-section-label" style="padding-left:4px;margin-bottom:8px">Licitaciones de Ejemplo</div>
          <div id="demo-list"></div>
        </div>
        <div id="demo-detail"></div>
      </div>
    </section>

    <!-- VISTA 3: ARQUITECTURA, PRIVACIDAD Y DESPLIEGUE -->
    <section id="view-arquitectura" class="hidden">
      <div class="hero-header">
        <div>
          <div class="eyebrow">Especificaciones Técnicas B2B</div>
          <h1 class="hero-title">Arquitectura Híbrida y Soberanía de Datos</h1>
          <p class="hero-subtitle">
            Separación estricta entre el motor matemático/documental local y la capa de razonamiento LLM configurable según los estándares de confidencialidad de cada mandante.
          </p>
        </div>
      </div>

      <div class="apple-table-wrap">
        <table class="apple-table">
          <thead>
            <tr>
              <th>Capa del Sistema</th>
              <th>Dónde se ejecuta</th>
              <th>Qué procesa</th>
              <th>Garantía de Confidencialidad</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td><strong>1. Motor Documental y Financiero (Python / .exe)</strong></td>
              <td>100% Local en el PC/Servidor del Cliente</td>
              <td>Lectura de correos <code>.eml</code>, descompresión <code>.zip</code>, cálculo de HH y márgenes en <code>costos.xlsx</code>, <code>matriz_cumplimiento.xlsx</code> y armado de <code>propuesta_tecnica.docx</code></td>
              <td>Las planillas de tarifas, costos internos y utilidades viven en el disco local y no requieren subir a nubes SaaS de terceros.</td>
            </tr>
            <tr>
              <td><strong>2A. Modo Cloud LLM Empresarial (Estándar)</strong></td>
              <td>API Comercial (Gemini / Claude / OpenAI)</td>
              <td>Interpretación de Términos de Referencia extensos, redacción metodológica y simulador de evaluación</td>
              <td>Operación bajo políticas empresariales <em>Zero-Data-Retention</em> (sin entrenamiento sobre datos del cliente).</td>
            </tr>
            <tr>
              <td><strong>2B. Modo Híbrido con Sanitización de Precios</strong></td>
              <td>Técnica en Cloud LLM + Económica 100% Local</td>
              <td>El LLM solo lee las bases técnicas públicas; el cálculo económico y el Acta de Aprobación corren solo en CPU local</td>
              <td>Aísla por completo la estrategia de precios y márgenes respecto de cualquier API externa.</td>
            </tr>
            <tr>
              <td><strong>2C. Modo Air-Gapped (LLM Local)</strong></td>
              <td>Servidor GPU Interno (Ollama / vLLM)</td>
              <td>Todo el flujo técnico y económico en red cerrada</td>
              <td>Operación 100% offline para contratos mineros o de infraestructura crítica con reserva estricta.</td>
            </tr>
          </tbody>
        </table>
      </div>
    </section>
  </main>
</div>

<!-- Modal Detalle de Habilidad -->
<div id="skill-modal" class="modal-backdrop hidden" onclick="closeSkillModal()">
  <div class="modal-sheet" onclick="event.stopPropagation()">
    <button class="close-pill" onclick="closeSkillModal()">Cerrar ✕</button>
    <h2 id="m-title"></h2>
    <div class="modal-meta" id="m-meta"></div>
    <div class="modal-section-title">Objetivo</div>
    <p id="m-obj" style="font-size:14px;line-height:1.5"></p>
    <div class="modal-section-title">Entradas</div>
    <ul id="m-ent"></ul>
    <div class="modal-section-title">Pasos de Ejecución</div>
    <ol id="m-pasos"></ol>
    <div class="modal-section-title">Entregable Verificable</div>
    <p id="m-sal" style="font-size:13px;font-weight:600;color:var(--accent)"></p>
    <div id="m-ctrl-box" class="hidden">
      <div class="modal-section-title">Punto de Control Humano</div>
      <p id="m-ctrl" style="font-size:13px;font-weight:600"></p>
    </div>
  </div>
</div>

<!-- Footer con créditos oficiales -->
<footer class="apple-footer">
  <div class="brand-cluster">
    <div class="brand-item">
      <span class="brand-caption">Desarrollado por</span>
      <img src="logo-tecknologia.png" alt="Tecknologia" class="logo-teck" />
    </div>
    <div class="brand-divider"></div>
    <div class="brand-item">
      <span class="brand-caption">Diseñado por</span>
      <img src="logo-geologgia.png" alt="Geologgia Ltda." class="logo-geologgia" />
    </div>
  </div>
  <div>BidFactory AI · 50 Habilidades Preconfiguradas para Ingeniería, Geología, Minería, Construcción y Energía</div>
</footer>

<script>
const SKILLS = {skills_json};
const FASES = {fases_json};
const DEMOS = {demos_json};
let activeDemoIdx = 0;

function renderSidebarAndPhases() {{
  const treeEl = document.getElementById('sidebar-tree');
  const gridEl = document.getElementById('phases-container');
  treeEl.innerHTML = '';
  gridEl.innerHTML = '';

  FASES.forEach(f => {{
    const habs = SKILLS.filter(s => s.f === f.id);
    const rangeTxt = `Habilidades ${{habs[0].n}}–${{habs[habs.length - 1].n}}`;

    // Sidebar group
    const group = document.createElement('div');
    group.className = 'tree-group';
    group.innerHTML = `
      <div class="tree-folder" onclick="this.nextElementSibling.classList.toggle('hidden')">
        <span>${{f.carpeta}}/</span>
        <span class="folder-badge">${{habs.length}}</span>
      </div>
      <div class="tree-children">
        ${{habs.map(h => `
          <div class="tree-leaf" onclick="openSkillModal(${{h.n}})">
            <span>habilidad-${{String(h.n).padStart(2, '0')}}.md</span>
            ${{[6,16,34,47,48].includes(h.n) ? '<span style="color:var(--accent)">●</span>' : ''}}
          </div>
        `).join('')}}
      </div>
    `;
    treeEl.appendChild(group);

    // Phase card
    const card = document.createElement('div');
    card.className = 'phase-card';
    card.innerHTML = `
      <div class="phase-card-header">
        <h3 class="phase-card-title">${{f.titulo}}</h3>
        <span class="phase-range-pill">${{rangeTxt}}</span>
      </div>
      <div>
        ${{habs.map(h => {{
          const isGate = [6,16,34,47,48].includes(h.n);
          return `
            <div class="skill-item" onclick="openSkillModal(${{h.n}})">
              <span class="skill-index">${{String(h.n).padStart(2, '0')}}</span>
              <span class="skill-label">${{h.nombre}}</span>
              ${{isGate ? '<span class="gate-pill">Control Aprobador</span>' : ''}}
            </div>
          `;
        }}).join('')}}
      </div>
    `;
    gridEl.appendChild(card);
  }});
}}

function openSkillModal(n) {{
  const s = SKILLS.find(x => x.n === n);
  if (!s) return;
  document.getElementById('m-title').textContent = `Habilidad ${{String(s.n).padStart(2, '0')}} · ${{s.nombre}}`;
  document.getElementById('m-meta').textContent = `Rol responsable: ${{s.rol}}` + (s.script ? `  |  Motor Python: ${{s.script}}` : '');
  document.getElementById('m-obj').textContent = s.obj;
  document.getElementById('m-ent').innerHTML = s.ent.map(e => `<li>${{e}}</li>`).join('');
  document.getElementById('m-pasos').innerHTML = s.pasos.map(p => `<li>${{p}}</li>`).join('');
  document.getElementById('m-sal').textContent = s.sal;
  const ctrlBox = document.getElementById('m-ctrl-box');
  if (s.control) {{
    ctrlBox.classList.remove('hidden');
    document.getElementById('m-ctrl').textContent = s.control;
  }} else {{
    ctrlBox.classList.add('hidden');
  }}
  document.getElementById('skill-modal').classList.remove('hidden');
}}

function closeSkillModal() {{
  document.getElementById('skill-modal').classList.add('hidden');
}}

function switchView(view) {{
  ['mapa', 'demo', 'arquitectura'].forEach(v => {{
    document.getElementById('view-' + v).classList.toggle('hidden', v !== view);
    document.getElementById('tab-' + v).classList.toggle('active', v === view);
  }});
}}

function renderDemoSection() {{
  const listEl = document.getElementById('demo-list');
  listEl.innerHTML = DEMOS.map((d, i) => `
    <div class="demo-item ${{i === activeDemoIdx ? 'active' : ''}}" onclick="selectDemo(${{i}})">
      <div class="demo-code">${{d.codigo}}</div>
      <div class="demo-name">${{d.nombre}}</div>
      <div class="demo-client">${{d.mandante}}</div>
    </div>
  `).join('');

  const d = DEMOS[activeDemoIdx];
  const esc = d.escenarios;
  const detailEl = document.getElementById('demo-detail');
  detailEl.innerHTML = `
    <div class="kpi-grid">
      <div class="kpi-box">
        <div class="kpi-title">Estado del Proceso</div>
        <div class="kpi-number" style="font-size:16px;margin-top:8px">${{d.estado_global}}</div>
        <div class="kpi-foot">Go/No-Go: ${{d.go_no_go_nota}}</div>
      </div>
      <div class="kpi-box">
        <div class="kpi-title">Puntaje Técnico Simulado (Hab. 45)</div>
        <div class="kpi-number">${{d.puntaje_simulado}} <span style="font-size:13px;font-weight:500;color:var(--label-tertiary)">/ 100</span></div>
        <div class="kpi-foot">Cumplimiento Matriz: ${{d.cumplimiento_pct}}%</div>
      </div>
      <div class="kpi-box">
        <div class="kpi-title">Esfuerzo y Plazo</div>
        <div class="kpi-number">${{d.hh_totales}} HH</div>
        <div class="kpi-foot">Plazo: ${{d.plazo_semanas}} semanas · ${{d.portal}}</div>
      </div>
      <div class="kpi-box">
        <div class="kpi-title">Precio Autorizado Aprobador (Hab. 48)</div>
        <div class="kpi-number" style="color:var(--accent)">${{esc.aprobado ? esc.aprobado.toLocaleString('es-CL') + ' UF' : 'Pendiente'}}</div>
        <div class="kpi-foot">Cierre: ${{d.cierre}}</div>
      </div>
    </div>

    <div class="apple-table-wrap">
      <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:12px;flex-wrap:wrap;gap:10px">
        <div>
          <h3 style="font-size:15px;font-weight:600">Escenarios Económicos para Decisión del Aprobador (Habilidad 34 / 48)</h3>
          <p style="font-size:12px;color:var(--label-secondary)">Costo Directo Base: <strong>${{esc.costo_directo.toLocaleString('es-CL')}} UF</strong> (${{d.hh_totales}} HH + Terreno/Subcontratos) + 12% Gastos Generales</p>
        </div>
        <button class="btn-primary-apple" onclick="simularAprobacion(${{activeDemoIdx}})">
          Firmar Acta de Aprobación (Demo)
        </button>
      </div>
      <table class="apple-table">
        <thead>
          <tr>
            <th>Escenario</th>
            <th>Contingencia</th>
            <th>Utilidad</th>
            <th>Precio Neto Oferta (UF)</th>
            <th>Acción Rápida</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td><strong>Escenario Agresivo</strong> (Alta competencia)</td>
            <td>3%</td>
            <td>12%</td>
            <td><strong>${{esc.agresivo.toLocaleString('es-CL')}} UF</strong></td>
            <td><button class="seg-btn" onclick="fijarPrecioDemo(${{activeDemoIdx}}, ${{esc.agresivo}})">Seleccionar</button></td>
          </tr>
          <tr>
            <td><strong>Escenario Objetivo Estándar</strong> (Recomendado)</td>
            <td>6%</td>
            <td>18%</td>
            <td><strong>${{esc.objetivo.toLocaleString('es-CL')}} UF</strong></td>
            <td><button class="seg-btn" onclick="fijarPrecioDemo(${{activeDemoIdx}}, ${{esc.objetivo}})">Seleccionar</button></td>
          </tr>
          <tr>
            <td><strong>Escenario Conservador</strong> (Alta complejidad / riesgo)</td>
            <td>10%</td>
            <td>25%</td>
            <td><strong>${{esc.conservador.toLocaleString('es-CL')}} UF</strong></td>
            <td><button class="seg-btn" onclick="fijarPrecioDemo(${{activeDemoIdx}}, ${{esc.conservador}})">Seleccionar</button></td>
          </tr>
        </tbody>
      </table>
    </div>

    <div class="apple-table-wrap">
      <h3 style="font-size:15px;font-weight:600;margin-bottom:10px">Matriz de Cumplimiento — ${{d.codigo}}</h3>
      <table class="apple-table">
        <thead>
          <tr>
            <th>ID</th>
            <th>Categoría</th>
            <th>Requisito Exigido en las Bases</th>
            <th>Fuente</th>
            <th>Inadmisibilidad</th>
            <th>Estado</th>
          </tr>
        </thead>
        <tbody>
          ${{d.requisitos.map(r => `
            <tr>
              <td><strong>${{r.id}}</strong></td>
              <td>${{r.cat}}</td>
              <td>${{r.req}}</td>
              <td style="color:var(--label-secondary)">${{r.fuente}}</td>
              <td>${{r.inadm ? '<strong>SÍ</strong>' : 'No'}}</td>
              <td><span class="badge-status ${{r.estado === 'Cumple' ? 'ok' : 'warn'}}">${{r.estado}}</span></td>
            </tr>
          `).join('')}}
        </tbody>
      </table>
    </div>
  `;
}}

function selectDemo(idx) {{
  activeDemoIdx = idx;
  renderDemoSection();
}}

function fijarPrecioDemo(idx, monto) {{
  DEMOS[idx].escenarios.aprobado = monto;
  DEMOS[idx].estado_global = 'APROBADA PARA ENVÍO';
  renderDemoSection();
}}

function simularAprobacion(idx) {{
  const d = DEMOS[idx];
  const sugerido = d.escenarios.aprobado || d.escenarios.objetivo;
  const val = prompt(`Aprobación Ejecutiva (Habilidad 48) — ${{d.codigo}}\\n\\nIngrese el Precio Neto Final Autorizado en UF:`, sugerido);
  if (val !== null && !isNaN(parseFloat(val))) {{
    fijarPrecioDemo(idx, parseFloat(val));
  }}
}}

function toggleTheme() {{
  const htmlEl = document.documentElement;
  const current = htmlEl.getAttribute('data-theme');
  const next = current === 'dark' ? 'light' : 'dark';
  htmlEl.setAttribute('data-theme', next);
  localStorage.setItem('bidfactory-theme', next);
  updateThemeButton(next);
}}

function updateThemeButton(theme) {{
  document.getElementById('theme-icon').textContent = theme === 'dark' ? '☀️' : '🌙';
  document.getElementById('theme-label').textContent = theme === 'dark' ? 'Modo Claro' : 'Modo Oscuro';
}}

(function init() {{
  const saved = localStorage.getItem('bidfactory-theme') || 'light';
  document.documentElement.setAttribute('data-theme', saved);
  updateThemeButton(saved);
  renderSidebarAndPhases();
  renderDemoSection();
}})();
</script>
</body>
</html>
"""
    (WEB_DIR / "index.html").write_text(html, encoding="utf-8")
    (ROOT / "panel_equipo_licitaciones.html").write_text(html, encoding="utf-8")
    shutil.copy2(BRAND_LOGOS / "logo-tecknologia.png", ROOT / "logo-tecknologia.png")
    shutil.copy2(BRAND_LOGOS / "logo-geologgia.png", ROOT / "logo-geologgia.png")
    print(f"[OK] Frontend Apple HIG Light/Dark generado en: {WEB_DIR / 'index.html'} y {ROOT / 'panel_equipo_licitaciones.html'}")


if __name__ == "__main__":
    generar_html_apple_hig()
