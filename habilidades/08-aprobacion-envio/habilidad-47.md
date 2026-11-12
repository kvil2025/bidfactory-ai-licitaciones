# Habilidad 47 — Informe al Revisor Final

**Fase:** VIII · Aprobación, envío y post-licitación  
**Rol responsable:** Bid Manager → Revisor Final  
**Scripts:** `informe_aprobacion.py`  

## Objetivo
Darle al Revisor Final todo lo necesario para decidir en 15 minutos.

## Entradas
- Matriz
- Observaciones QA
- Evaluación simulada
- Precio recomendado

## Pasos
1. Ejecutar `python scripts/informe_aprobacion.py <CODIGO>` → `revision/informe_revisor_final.docx`.
2. Contenido: resumen de la licitación, estado de cumplimiento (% y pendientes), puntaje técnico simulado, precio y margen por escenario, riesgos principales, desviaciones declaradas, observaciones QA abiertas, checklist de envío.
3. Recomendación clara: APROBAR / APROBAR CON CAMBIOS / NO ENVIAR.

## Salida
Informe para el Revisor Final.

## Punto de control
🔴 **PUNTO DE CONTROL HUMANO — REVISOR FINAL (Carlos)**: revisa el informe, pide cambios o da el visto bueno.

## Reglas generales
- Citar siempre la fuente (documento, numeral, página) de cada dato extraído de las bases.
- No inventar experiencia, certificados ni cifras. Si falta información, marcar `[COMPLETAR]` y preguntar.
- Actualizar `estado.json` al terminar la habilidad.
