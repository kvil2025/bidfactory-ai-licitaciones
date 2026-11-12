# Habilidad 05 — Registro en la cartera de licitaciones

**Fase:** I · Recepción y triaje  
**Rol responsable:** Bid Manager  
**Scripts:** `cartera.py`  

## Objetivo
Mantener una vista única de todas las licitaciones activas, enviadas, adjudicadas y perdidas.

## Entradas
- ficha.json de cada licitación

## Pasos
1. Ejecutar `python scripts/cartera.py` para regenerar `cartera_licitaciones.xlsx`.
2. Verificar estado: RECIBIDA → GO/NO-GO → EN PREPARACION → EN REVISION → APROBADA → ENVIADA → ADJUDICADA/PERDIDA/DESISTIDA.

## Salida
`cartera_licitaciones.xlsx` actualizado.

## Reglas generales
- Citar siempre la fuente (documento, numeral, página) de cada dato extraído de las bases.
- No inventar experiencia, certificados ni cifras. Si falta información, marcar `[COMPLETAR]` y preguntar.
- Actualizar `estado.json` al terminar la habilidad.
