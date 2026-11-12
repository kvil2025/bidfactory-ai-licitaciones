# Equipo de Licitaciones IA — Geologgia Ltda.

Sistema integral de **50 habilidades preconfiguradas (`habilidad-01.md` a `habilidad-50.md`)**, **1 Orquestador (`00-bid-manager/SKILL.md`)**, **Base de Conocimiento real de Geologgia** y **7 scripts en Python** que automatizan de punta a punta el ciclo de licitaciones de **geología, geotecnia, túneles, minería, construcción y energía**, desde que llega el correo de invitación hasta el **Revisor Final y Aprobador de envío** (Carlos Cristian Ávila Elgueta).

---

## 1. Arquitectura de Carpetas

```text
equipo_licitaciones/
├── README.md                           # Este manual operativo
├── cartera_licitaciones.xlsx           # Tablero general consolidado (generado por scripts/cartera.py)
├── 00-bid-manager/
│   └── SKILL.md                        # Orquestador del equipo + reglas y puntos de control humanos
├── habilidades/                        # Las 50 habilidades en 8 fases + INDICE.md
│   ├── INDICE.md
│   ├── 01-recepcion-triaje/            # Habilidades 01 a 06 (Correo, orden de bases, ficha, calendario, Go/No-Go)
│   ├── 02-analisis-bases/              # Habilidades 07 a 13 (Requisitos ADM/TEC, Matriz, Criterios, Garantías, Riesgos)
│   ├── 03-consultas-aclaraciones/      # Habilidades 14 a 19 (Hallazgos, preguntas al mandante, respuestas, adendas)
│   ├── 04-propuesta-tecnica/           # Habilidades 20 a 28 (Comprensión, metodología, Gantt, equipo, CVs, HSE, QA/QC, mapas)
│   ├── 05-propuesta-economica/         # Habilidades 29 a 35 (EDT, HH por rol, costos directos, GG, formulario, sensibilidad)
│   ├── 06-documentacion-legal/         # Habilidades 36 a 40 (Anexos, declaraciones, garantía seriedad, certificados, firmas)
│   ├── 07-revision-qa/                 # Habilidades 41 a 46 (Cruce matriz, revisión par, evaluador simulado, estilo y formato)
│   └── 08-aprobacion-envio/            # Habilidades 47 a 50 (Informe Revisor Final, Acta Aprobador, Envío, Post-licitación)
├── base_conocimiento/
│   ├── empresa.md                      # Datos legales y societarios de Geologgia Ltda.
│   ├── experiencia_geologgia.md        # Track record verificado (7 centrales hidroeléctricas, ~80 km túneles civiles, ~20 km mineros, Codelco, BHP)
│   ├── equipo.md                       # Perfiles clave y especialistas
│   └── tarifas.md                      # Tarifas UF/HH, costos directos de terreno y parámetros de GG/contingencia/utilidad
├── plantillas/
│   ├── ficha_licitacion.json           # Esquema estándar de licitación
│   ├── requisitos_ejemplo.json         # Esquema de requisitos ADM/TEC/EXP/ECO y criterios de evaluación
│   ├── go_no_go.md                     # Matriz ponderada de decisión Go/No-Go
│   └── checklist_administrativo.md     # Checklist de sobre administrativo y garantías
├── scripts/
│   ├── leer_correos.py                 # Lee correos (.eml o Gmail IMAP) y genera borradores .eml de consultas
│   ├── nueva_licitacion.py             # Crea toda la estructura de una licitación nueva
│   ├── extraer_texto.py                # Extrae texto de PDF/DOCX de las bases y detecta anexos faltantes
│   ├── matriz_cumplimiento.py          # Genera matriz_cumplimiento.xlsx (3 hojas con fórmulas y semáforo)
│   ├── plantilla_costos.py             # Genera costos.xlsx (Escenarios Agresivo/Objetivo/Conservador + HH + Directos)
│   ├── armar_propuesta.py              # Compila propuesta_tecnica_<CODIGO>.docx y ejecuta auditor QA (--verificar)
│   ├── informe_aprobacion.py           # Genera informe_revisor_final.docx y emite acta_aprobacion.md
│   ├── cartera.py                      # Consolida todas las licitaciones en cartera_licitaciones.xlsx
│   └── demo_ciclo_completo.py          # Prueba automatizada de punta a punta (Habilidades 01 a 50)
└── licitaciones/
    └── LIC-2026-001/                   # Licitación de demostración generada de punta a punta
```

---

## 2. Flujo Rápido de Uso (Paso a Paso)

### Paso 1 — Llega un correo de invitación o bases (Habilidades 01–06)
```powershell
# Opción A: desde un correo descargado (.eml)
python scripts/leer_correos.py --eml ruta/al/correo.eml

# Opción B: buscando en Gmail por IMAP (solo lectura)
python scripts/leer_correos.py --imap --dias 7

# Opción C: crear manualmente la licitación
python scripts/nueva_licitacion.py LIC-2026-002 "Asesoría Geotécnica Túneles" "Codelco"
```

### Paso 2 — Extraer texto de bases y generar Matriz de Cumplimiento en Excel (Habilidades 07–13)
```powershell
python scripts/extraer_texto.py LIC-2026-001
python scripts/matriz_cumplimiento.py LIC-2026-001 --resumen
```
Genera `licitaciones/LIC-2026-001/analisis/matriz_cumplimiento.xlsx` con 3 pestañas (`Matriz_Cumplimiento`, `Resumen_QA` y `Criterios_Evaluacion`).

### Paso 3 — Preparar borrador de consultas al mandante (Habilidades 14–19)
```powershell
python scripts/leer_correos.py --borrador-consultas LIC-2026-001 --ronda 1
```
Crea `consultas/BORRADOR_consultas_ronda_1.eml` listo para que Carlos lo revise y envíe.

### Paso 4 — Generar Propuesta Económica en Excel y Propuesta Técnica en Word (Habilidades 20–46)
```powershell
python scripts/plantilla_costos.py LIC-2026-001
python scripts/armar_propuesta.py LIC-2026-001 --verificar
```
- Excel económico: `licitaciones/LIC-2026-001/propuesta/economica/costos.xlsx`
- Word técnico: `licitaciones/LIC-2026-001/propuesta/propuesta_tecnica_LIC-2026-001.docx`
- Auditoría QA de formato y no-filtración de precios: `licitaciones/LIC-2026-001/revision/verificacion_estilo_y_formato.md`

### Paso 5 — Informe para Revisor Final, Aprobación de Envío y Cartera (Habilidades 47–50)
```powershell
# Generar el informe ejecutivo Word para revisión de Carlos Ávila:
python scripts/informe_aprobacion.py LIC-2026-001

# Una vez revisado, emitir el Acta de Aprobación con el precio definitivo:
python scripts/informe_aprobacion.py LIC-2026-001 --aprobar --precio 853.73 --moneda UF --por "Carlos Cristian Ávila Elgueta"

# Actualizar el tablero general de licitaciones:
python scripts/cartera.py
```
