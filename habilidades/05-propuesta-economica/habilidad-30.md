# Habilidad 30 — Estimación de HH por rol

**Fase:** V · Propuesta económica  
**Rol responsable:** Estimador de Costos  

## Objetivo
Calcular las horas profesionales necesarias de forma realista.

## Entradas
- EDT
- Gantt
- Equipo propuesto

## Pasos
1. Asignar HH por partida y rol (jefe de proyecto, geólogo senior, geólogo junior, geotécnico, SIG, dibujante, técnico de terreno).
2. Usar las tarifas de `base_conocimiento/tarifas.md` (UF/HH o CLP/HH).
3. Verificar coherencia con la dedicación declarada en el equipo y con el Gantt.

## Salida
Hoja HH de `costos.xlsx`.

## Reglas generales
- Citar siempre la fuente (documento, numeral, página) de cada dato extraído de las bases.
- No inventar experiencia, certificados ni cifras. Si falta información, marcar `[COMPLETAR]` y preguntar.
- Actualizar `estado.json` al terminar la habilidad.
