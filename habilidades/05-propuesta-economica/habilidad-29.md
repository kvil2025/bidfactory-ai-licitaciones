# Habilidad 29 — Desglose de actividades (EDT)

**Fase:** V · Propuesta económica  
**Rol responsable:** Estimador de Costos  
**Scripts:** `plantilla_costos.py`  

## Objetivo
Estructurar el costo en la misma lógica que el alcance y el formulario del mandante.

## Entradas
- TdR
- Formulario económico del mandante
- Metodología

## Pasos
1. Crear la EDT con las partidas del formulario del mandante (si existe) o según el TdR.
2. Para cada partida: unidad (gl, m, un, HH, día) y cantidad.
3. Registrar en `propuesta/economica/costos.xlsx` (generado con `python scripts/plantilla_costos.py <CODIGO>`).

## Salida
EDT con cantidades.

## Reglas generales
- Citar siempre la fuente (documento, numeral, página) de cada dato extraído de las bases.
- No inventar experiencia, certificados ni cifras. Si falta información, marcar `[COMPLETAR]` y preguntar.
- Actualizar `estado.json` al terminar la habilidad.
