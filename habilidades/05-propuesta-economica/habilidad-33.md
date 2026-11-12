# Habilidad 33 — Formulario económico del mandante

**Fase:** V · Propuesta económica  
**Rol responsable:** Estimador de Costos  

## Objetivo
Traspasar el precio al formato oficial sin errores.

## Entradas
- costos.xlsx
- Formulario oficial

## Pasos
1. Completar el formulario exactamente como se exige (moneda, IVA incluido o no, decimales, reajustabilidad).
2. Verificar sumas y que cada precio unitario × cantidad = total.
3. Comprobar que el total coincide con `costos.xlsx` y que no supera el presupuesto referencial/máximo.

## Salida
Formulario económico completo.

## Punto de control
Un error aritmético o de moneda puede dejar la oferta fuera de bases.

## Reglas generales
- Citar siempre la fuente (documento, numeral, página) de cada dato extraído de las bases.
- No inventar experiencia, certificados ni cifras. Si falta información, marcar `[COMPLETAR]` y preguntar.
- Actualizar `estado.json` al terminar la habilidad.
