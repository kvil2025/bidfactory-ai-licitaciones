# Habilidad 41 — Revisión de cumplimiento vs. matriz

**Fase:** VII · Revisión y control de calidad  
**Rol responsable:** Revisor QA  
**Scripts:** `matriz_cumplimiento.py --resumen`  

## Objetivo
Confirmar que cada requisito de la matriz está respondido y localizable.

## Entradas
- matriz_cumplimiento.xlsx
- Documentos de la oferta

## Pasos
1. Para cada requisito, abrir el documento indicado y verificar que la respuesta existe y es suficiente.
2. Actualizar el estado a Cumple / Cumple con desviación / No cumple.
3. Cualquier 'No cumple' de un requisito causal de inadmisibilidad bloquea el envío.

## Salida
Matriz con 100 % revisado.

## Reglas generales
- Citar siempre la fuente (documento, numeral, página) de cada dato extraído de las bases.
- No inventar experiencia, certificados ni cifras. Si falta información, marcar `[COMPLETAR]` y preguntar.
- Actualizar `estado.json` al terminar la habilidad.
