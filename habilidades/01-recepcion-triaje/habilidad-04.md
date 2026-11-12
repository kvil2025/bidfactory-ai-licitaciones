# Habilidad 04 — Calendario de hitos

**Fase:** I · Recepción y triaje  
**Rol responsable:** Bid Manager  

## Objetivo
Ninguna fecha se pierde: visita a terreno, consultas, respuestas, cierre técnico y económico, apertura.

## Entradas
- Bases (sección cronograma)
- ficha.json

## Pasos
1. Extraer todas las fechas y horas con su zona horaria (Chile continental).
2. Registrar en `ficha.json > hitos` y en `analisis/calendario.md` como tabla.
3. Calcular fechas internas hacia atrás: borrador técnico (cierre −5 días hábiles), económico (−4), QA (−3), revisión final (−2), aprobación (−1), envío (cierre −1 día, nunca el último minuto).
4. Ofrecer al usuario crear los eventos en su calendario.

## Salida
Calendario con hitos externos + internos.

## Punto de control
Si faltan menos de 5 días hábiles al cierre, marcar la licitación como **URGENTE** en `estado.json`.

## Reglas generales
- Citar siempre la fuente (documento, numeral, página) de cada dato extraído de las bases.
- No inventar experiencia, certificados ni cifras. Si falta información, marcar `[COMPLETAR]` y preguntar.
- Actualizar `estado.json` al terminar la habilidad.
