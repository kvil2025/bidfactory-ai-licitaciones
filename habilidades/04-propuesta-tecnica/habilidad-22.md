# Habilidad 22 — Plan de trabajo y Carta Gantt

**Fase:** IV · Propuesta técnica  
**Rol responsable:** Especialista Técnico + Bid Manager  
**Scripts:** `armar_propuesta.py`  

## Objetivo
Mostrar un plan realista que cumple el plazo exigido.

## Entradas
- Metodología
- Plazo de las bases

## Pasos
1. Definir actividades, duraciones, dependencias e hitos de entregables.
2. Registrar en `propuesta/gantt.csv` (actividad, inicio_semana, duracion_semanas, responsable).
3. `armar_propuesta.py` lo convierte en una tabla Gantt en el Word.
4. Verificar coherencia con HH (hab. 30) y con la ventana climática (invierno altiplánico, nieve en cordillera).

## Salida
Gantt + texto del plan de trabajo.

## Reglas generales
- Citar siempre la fuente (documento, numeral, página) de cada dato extraído de las bases.
- No inventar experiencia, certificados ni cifras. Si falta información, marcar `[COMPLETAR]` y preguntar.
- Actualizar `estado.json` al terminar la habilidad.
