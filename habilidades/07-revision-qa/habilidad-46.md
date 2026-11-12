# Habilidad 46 — Corrección de estilo, formato y foliado

**Fase:** VII · Revisión y control de calidad  
**Rol responsable:** Revisor QA  
**Scripts:** `armar_propuesta.py --verificar`  

## Objetivo
Una oferta impecable: sin errores ortográficos, con formato consistente y profesional.

## Entradas
- Word final

## Pasos
1. Regenerar el Word con `python scripts/armar_propuesta.py <CODIGO>`.
2. Revisar ortografía, numeración de secciones, figuras y tablas, índice, encabezados con nombre de la licitación, logos.
3. Verificar que no queden marcadores `[COMPLETAR]`, `TODO` o nombres de otros mandantes (`armar_propuesta.py --verificar`).

## Salida
Propuesta técnica final (DOCX/PDF).

## Reglas generales
- Citar siempre la fuente (documento, numeral, página) de cada dato extraído de las bases.
- No inventar experiencia, certificados ni cifras. Si falta información, marcar `[COMPLETAR]` y preguntar.
- Actualizar `estado.json` al terminar la habilidad.
