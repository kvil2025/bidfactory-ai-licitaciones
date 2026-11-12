# Habilidad 09 — Matriz de cumplimiento

**Fase:** II · Análisis de bases  
**Rol responsable:** Analista de Bases  
**Scripts:** `matriz_cumplimiento.py`  

## Objetivo
Una sola tabla que demuestra que la oferta responde a TODO lo exigido.

## Entradas
- `analisis/requisitos.json` (hab. 7, 8, 10–13)

## Pasos
1. Ejecutar `python scripts/matriz_cumplimiento.py <CODIGO>`.
2. Se genera `analisis/matriz_cumplimiento.xlsx` con hojas: Matriz, Resumen, Criterios de evaluación.
3. Cada requisito tendrá: responsable, documento de la oferta donde se responde, estado (Pendiente / En curso / Cumple / Cumple con desviación / No cumple) y observaciones.
4. La matriz es el documento vivo del proceso: se actualiza en las hab. 19, 41 y 47.

## Salida
`matriz_cumplimiento.xlsx`.

## Reglas generales
- Citar siempre la fuente (documento, numeral, página) de cada dato extraído de las bases.
- No inventar experiencia, certificados ni cifras. Si falta información, marcar `[COMPLETAR]` y preguntar.
- Actualizar `estado.json` al terminar la habilidad.
