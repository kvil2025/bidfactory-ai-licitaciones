# Habilidad 07 — Extracción de requisitos administrativos

**Fase:** II · Análisis de bases  
**Rol responsable:** Analista de Bases  

## Objetivo
Listar cada requisito administrativo/formal exigido, con su fuente exacta.

## Entradas
- BAG / bases administrativas

## Pasos
1. Recorrer las bases y extraer cada exigencia: documentos, formatos, firmas, idioma, número de copias, forma de entrega, vigencia de la oferta.
2. Para cada uno: ID (ADM-001…), texto literal, documento y numeral/página, si es causal de inadmisibilidad (SÍ/NO).
3. Guardar en `analisis/requisitos.json` (formato en `plantillas/requisitos_ejemplo.json`).

## Salida
Requisitos ADM en `requisitos.json`.

## Reglas generales
- Citar siempre la fuente (documento, numeral, página) de cada dato extraído de las bases.
- No inventar experiencia, certificados ni cifras. Si falta información, marcar `[COMPLETAR]` y preguntar.
- Actualizar `estado.json` al terminar la habilidad.
