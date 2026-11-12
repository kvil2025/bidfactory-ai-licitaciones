# Habilidad 43 — Revisión económica

**Fase:** VII · Revisión y control de calidad  
**Rol responsable:** Revisor QA  

## Objetivo
Verificar aritmética, consistencia y razonabilidad del precio.

## Entradas
- costos.xlsx
- Formulario económico

## Pasos
1. Recalcular totales; revisar IVA, moneda, UF del día, decimales.
2. Comparar ratios con licitaciones anteriores ($/m de sondaje, HH totales/MUSD, % de terreno).
3. Revisar que toda cotización esté vigente al inicio estimado del contrato.

## Salida
`revision/observaciones_economicas.md`.

## Reglas generales
- Citar siempre la fuente (documento, numeral, página) de cada dato extraído de las bases.
- No inventar experiencia, certificados ni cifras. Si falta información, marcar `[COMPLETAR]` y preguntar.
- Actualizar `estado.json` al terminar la habilidad.
