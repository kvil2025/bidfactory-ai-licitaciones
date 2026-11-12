# Habilidad 48 — Aprobación y registro de la decisión

**Fase:** VIII · Aprobación, envío y post-licitación  
**Rol responsable:** Aprobador  

## Objetivo
Dejar registro formal de quién aprobó qué, cuándo y con qué precio.

## Entradas
- Informe al Revisor Final

## Pasos
1. El Aprobador indica: decisión, precio final aprobado, condiciones.
2. Registrar con `python scripts/informe_aprobacion.py <CODIGO> --aprobar --precio <MONTO> --por "<Nombre>"`.
3. Se guarda en `estado.json > aprobacion` y en `revision/acta_aprobacion.md` con fecha y hora.

## Salida
Acta de aprobación.

## Punto de control
🔴 **PUNTO DE CONTROL HUMANO — APROBADOR (Carlos)**. Sin acta no hay envío.

## Reglas generales
- Citar siempre la fuente (documento, numeral, página) de cada dato extraído de las bases.
- No inventar experiencia, certificados ni cifras. Si falta información, marcar `[COMPLETAR]` y preguntar.
- Actualizar `estado.json` al terminar la habilidad.
