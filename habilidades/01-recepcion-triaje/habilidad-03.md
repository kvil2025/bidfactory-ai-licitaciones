# Habilidad 03 — Ficha resumen de la licitación

**Fase:** I · Recepción y triaje  
**Rol responsable:** Analista de Bases  

## Objetivo
Resumir en una página qué se licita, para quién, cuándo y con qué condiciones clave.

## Entradas
- Texto de bases (`analisis/texto/`)

## Pasos
1. Completar `ficha.json` (plantilla en `plantillas/ficha_licitacion.json`): mandante, código, objeto, ubicación, región, modalidad (pública/privada/invitación), tipo de contrato (suma alzada, serie de precios, HH), plazo de ejecución, presupuesto referencial, moneda, garantías, visita a terreno, fecha de cierre.
2. Clasificar la disciplina: geología / geotecnia / hidrogeología / minería / túneles / construcción / energía / medio ambiente / claims.
3. Redactar un resumen ejecutivo de 5 líneas en `analisis/ficha_resumen.md`.

## Salida
`licitaciones/<CODIGO>/ficha.json` + `analisis/ficha_resumen.md`.

## Reglas generales
- Citar siempre la fuente (documento, numeral, página) de cada dato extraído de las bases.
- No inventar experiencia, certificados ni cifras. Si falta información, marcar `[COMPLETAR]` y preguntar.
- Actualizar `estado.json` al terminar la habilidad.
