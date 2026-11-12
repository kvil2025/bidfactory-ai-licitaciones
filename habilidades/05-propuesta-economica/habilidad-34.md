# Habilidad 34 — Análisis de sensibilidad y precio objetivo

**Fase:** V · Propuesta económica  
**Rol responsable:** Estimador de Costos → Aprobador  

## Objetivo
Definir el precio con conocimiento del margen, del riesgo y de la competencia.

## Entradas
- costos.xlsx
- Criterios de evaluación (fórmula de precio)
- Historial de adjudicaciones (Mercado Público)

## Pasos
1. Escenarios: precio mínimo (costo + utilidad mínima), objetivo y agresivo.
2. Simular el puntaje económico con la fórmula de las bases frente a precios probables de la competencia.
3. Analizar la sensibilidad a ±20 % en metros de sondaje, días de terreno y tipo de cambio.
4. Recomendar un precio en `revision/precio_recomendado.md`.

## Salida
Recomendación de precio.

## Punto de control
🔴 El precio final lo decide el Aprobador (hab. 48).

## Reglas generales
- Citar siempre la fuente (documento, numeral, página) de cada dato extraído de las bases.
- No inventar experiencia, certificados ni cifras. Si falta información, marcar `[COMPLETAR]` y preguntar.
- Actualizar `estado.json` al terminar la habilidad.
