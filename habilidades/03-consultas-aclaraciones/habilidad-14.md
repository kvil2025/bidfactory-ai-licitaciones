# Habilidad 14 — Detección de ambigüedades y vacíos

**Fase:** III · Consultas y aclaraciones  
**Rol responsable:** Analista de Bases + Especialista Técnico  

## Objetivo
Encontrar lo que no está claro antes de que sea un problema en la oferta o en el contrato.

## Entradas
- requisitos.json
- riesgos_contractuales.md

## Pasos
1. Buscar: contradicciones entre documentos, cantidades sin definir, información geológica de base faltante (sondajes previos, estudios anteriores, acceso), criterios sin fórmula, plazos imposibles, responsabilidades indefinidas (permisos, accesos, servidumbres, agua, energía en faena).
2. Listar cada hallazgo con referencia y por qué importa (impacto en precio, plazo o riesgo).

## Salida
`consultas/hallazgos.md`.

## Reglas generales
- Citar siempre la fuente (documento, numeral, página) de cada dato extraído de las bases.
- No inventar experiencia, certificados ni cifras. Si falta información, marcar `[COMPLETAR]` y preguntar.
- Actualizar `estado.json` al terminar la habilidad.
