# Habilidad 19 — Actualización de la matriz tras aclaraciones

**Fase:** III · Consultas y aclaraciones  
**Rol responsable:** Analista de Bases  
**Scripts:** `matriz_cumplimiento.py`  

## Objetivo
Mantener la matriz de cumplimiento al día con respuestas y adendas.

## Entradas
- impacto_respuestas.md
- registro_adendas.md

## Pasos
1. Actualizar `requisitos.json` (agregar, modificar o anular requisitos, citando la fuente: 'Adenda 2, resp. 14').
2. Regenerar la matriz: `python scripts/matriz_cumplimiento.py <CODIGO>` (conserva estados ya ingresados).

## Salida
Matriz actualizada.

## Reglas generales
- Citar siempre la fuente (documento, numeral, página) de cada dato extraído de las bases.
- No inventar experiencia, certificados ni cifras. Si falta información, marcar `[COMPLETAR]` y preguntar.
- Actualizar `estado.json` al terminar la habilidad.
