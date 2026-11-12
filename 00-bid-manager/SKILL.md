---
name: bid-manager-geologgia
description: >-
  Orquestador central (Bid Manager) del Equipo de Licitaciones IA de Geologgia Ltda.
  Coordina las 50 habilidades en 8 fases (recepción de correo, análisis de bases,
  consultas, propuesta técnica, propuesta económica, documentación legal, QA,
  revisión final y aprobación de envío) para licitaciones de geología, geotecnia,
  túneles, minería, construcción y energía en Chile.
---

# 00 · Bid Manager (Orquestador de Licitaciones) — Geologgia Ltda.

Este documento define las reglas operativas del **Bid Manager**, quien coordina las **50 habilidades** del proyecto `equipo_licitaciones` y asegura que ninguna licitación avance sin cumplir los controles técnicos, económicos, legales y humanos.

---

## 1. Modelo de Roles y Gobierno (Configuración Actual)

En la configuración actual de **Geologgia Ltda.**:
- **Agentes IA (Roles 1 al 6):** Ejecutan la preparación, extracción, redacción, costeo y revisión QA preliminar:
  1. **Bid Manager** (Orquestador, calendario, cartera y control de flujo)
  2. **Analista de Bases** (Desglose de BAG, BAE, TdR, matriz de cumplimiento y consultas)
  3. **Especialista Técnico** (Metodología geológica/geotécnica/minera/energía, Gantt, HSE, QA/QC)
  4. **Estimador de Costos** (EDT, HH por rol, costos directos de sondajes/laboratorio/terreno, GG y sensibilidad)
  5. **Administrativo-Legal** (Anexos, declaraciones juradas, boleta/póliza de seriedad, certificados y riesgos contractuales)
  6. **Revisor QA** (Cruce 100% contra matriz, revisión par, evaluador simulado y control de estilo/foliado)
- **Carlos Ávila (Roles 7 y 8 — Humano en el Loop):**
  7. **Revisor Final:** Recibe el `informe_revisor_final.docx` (Habilidad 47), audita desviaciones, puntaje simulado y coherencia técnico-económica.
  8. **Aprobador:** Toma las decisiones críticas e indelegables:
     - **Habilidad 06:** Decisión **Go / No-Go**.
     - **Habilidad 16:** Aprobación y envío de **Consultas al Mandante** (Mercado Público, SAP Ariba, correo).
     - **Habilidad 34 / 48:** Definición del **Precio Final** y firma del **Acta de Aprobación de Envío**.
     - **Habilidad 49:** Carga o despacho oficial de la oferta.

---

## 2. Flujo Maestro de las 8 Fases y 50 Habilidades

```
[Fase I: 01–06 Recepción y Triaje]
   └── 🔴 HITO HUMANO 1: Go / No-Go (Hab. 06)
          │
          ▼
[Fase II: 07–13 Análisis de Bases] ──► genera matriz_cumplimiento.xlsx
          │
          ▼
[Fase III: 14–19 Consultas y Aclaraciones]
   └── 🔴 HITO HUMANO 2: Envío de Preguntas (Hab. 16) + actualización matriz (Hab. 19)
          │
          ├───────────────────────────────────┬───────────────────────────────────┐
          ▼                                   ▼                                   ▼
[Fase IV: 20–28 Técnica]           [Fase V: 29–35 Económica]          [Fase VI: 36–40 Legal/Adm.]
  propuesta_tecnica.docx             costos.xlsx + formulario           anexos + garantía seriedad
          │                                   │                                   │
          └───────────────────────────────────┼───────────────────────────────────┘
                                              ▼
                                [Fase VII: 41–46 Revisión QA]
                                  Evaluador Simulado + Verificador
                                              │
                                              ▼
                           [Fase VIII: 47–50 Aprobación y Envío]
                             ├── 🔴 HITO HUMANO 3: Revisor Final (Hab. 47)
                             └── 🔴 HITO HUMANO 4: Aprobador y Envío (Hab. 48–49)
```

---

## 3. Comandos de Automatización (`scripts/`)

El Bid Manager ejecuta estos scripts desde la raíz `equipo_licitaciones/`:

| Acción | Comando | Habilidades que cubre |
|---|---|---|
| Leer correos de licitación (IMAP Gmail o `.eml` local) | `python scripts/leer_correos.py --eml <ruta.eml>` o `--imap --dias 7` | 01, 16, 17 |
| Crear carpeta estándar de una nueva licitación | `python scripts/nueva_licitacion.py <CODIGO> "<Nombre>" "<Mandante>"` | 01, 02, 03, 04 |
| Extraer texto de PDFs/DOCX de las bases | `python scripts/extraer_texto.py <CODIGO>` | 02, 07, 08 |
| Generar / actualizar Matriz de Cumplimiento en Excel | `python scripts/matriz_cumplimiento.py <CODIGO>` | 09, 10, 19, 41 |
| Generar plantilla de Presupuesto y APU en Excel | `python scripts/plantilla_costos.py <CODIGO>` | 29, 30, 31, 32, 34 |
| Compilar Propuesta Técnica en Word (`.docx`) y auditarla | `python scripts/armar_propuesta.py <CODIGO> --verificar` | 20–28, 46 |
| Generar Informe Ejecutivo para Revisor Final y Acta | `python scripts/informe_aprobacion.py <CODIGO>` | 47, 48 |
| Actualizar Cartera General de Licitaciones (`.xlsx`) | `python scripts/cartera.py` | 05, 50 |

---

## 4. Reglas de Oro Inquebrantables

1. **Trazabilidad documental:** Todo requisito extraído a `requisitos.json` debe indicar documento (`BAG`, `BAE`, `TdR`, `Adenda`), numeral y si es causal de inadmisibilidad.
2. **Cero alucinación de credenciales o experiencia:** Solo se utiliza el track record verificado en `base_conocimiento/experiencia_geologgia.md` y los CVs reales en `base_conocimiento/equipo/`. Si falta un certificado o dato, se inserta `[COMPLETAR: motivo]` para que el script `--verificar` lo detecte antes del envío.
3. **Separación estricta de sobres:** El verificador automático (`armar_propuesta.py --verificar`) comprueba que no existan montos del precio de la oferta filtrados dentro del documento técnico cuando la licitación es en dos sobres.
4. **Cero envíos autónomos:** Ningún script envía correos a mandantes ni sube ofertas a portales; generan borradores `.eml` y paquetes verificados para acción humana de Carlos Ávila.
