# Habilidad 11 — Garantías y seguros exigidos

**Fase:** II · Análisis de bases  
**Rol responsable:** Administrativo-Legal  

## Objetivo
Identificar a tiempo garantías y seguros (requieren gestión bancaria con días de anticipación).

## Entradas
- Bases administrativas
- Borrador de contrato

## Pasos
1. Extraer: garantía de seriedad (monto, glosa exacta, beneficiario, RUT, vigencia, instrumento aceptado: boleta, vale vista, póliza, certificado de fianza), garantía de fiel cumplimiento, anticipo, seguros RC / accidentes.
2. Registrar como requisitos ADM críticos.
3. Generar `analisis/garantias.md` con instrucciones listas para el banco o la aseguradora.

## Salida
Ficha de garantías.

## Punto de control
Si la garantía de seriedad no se puede emitir antes del cierre, alertar de inmediato (riesgo de inadmisibilidad).

## Reglas generales
- Citar siempre la fuente (documento, numeral, página) de cada dato extraído de las bases.
- No inventar experiencia, certificados ni cifras. Si falta información, marcar `[COMPLETAR]` y preguntar.
- Actualizar `estado.json` al terminar la habilidad.
