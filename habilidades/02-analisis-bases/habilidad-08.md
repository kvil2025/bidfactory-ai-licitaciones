# Habilidad 08 — Extracción de requisitos técnicos (TdR)

**Fase:** II · Análisis de bases  
**Rol responsable:** Analista de Bases + Especialista Técnico  

## Objetivo
Desglosar el alcance técnico en requisitos verificables.

## Entradas
- TdR / bases técnicas / especificaciones / planos

## Pasos
1. Extraer alcance, actividades, cantidades (m de sondaje, n° de ensayos, km de mapeo, calicatas), normas exigidas (NCh, ASTM, ISRM, NCh433, DS61, ICOLD, etc.), entregables, formatos (shapefile, DWG, informe), plazos parciales.
2. ID TEC-001…, texto literal, referencia, criticidad.
3. Marcar requisitos que exigen equipos o subcontratos (perforación, laboratorio, geofísica, topografía).

## Salida
Requisitos TEC en `requisitos.json`.

## Reglas generales
- Citar siempre la fuente (documento, numeral, página) de cada dato extraído de las bases.
- No inventar experiencia, certificados ni cifras. Si falta información, marcar `[COMPLETAR]` y preguntar.
- Actualizar `estado.json` al terminar la habilidad.
