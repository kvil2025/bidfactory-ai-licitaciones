# Habilidad 16 — Envío y registro de consultas

**Fase:** III · Consultas y aclaraciones  
**Rol responsable:** Bid Manager → Aprobador  

## Objetivo
Enviar las consultas dentro de plazo por el canal correcto y dejar evidencia.

## Entradas
- preguntas_ronda_N.md

## Pasos
1. Confirmar canal: foro de Mercado Público, portal privado o correo al contacto oficial (nunca a contactos no autorizados en las bases).
2. Preparar borrador del correo con `python scripts/leer_correos.py --borrador-consultas <CODIGO> <N>` (crea un .eml, no envía).
3. Tras el envío por el usuario, guardar comprobante en `consultas/` y registrar fecha en `estado.json`.

## Salida
Consultas enviadas + comprobante.

## Punto de control
🔴 **PUNTO DE CONTROL HUMANO**: el Aprobador revisa y envía. La IA nunca envía correos al mandante por sí sola.

## Reglas generales
- Citar siempre la fuente (documento, numeral, página) de cada dato extraído de las bases.
- No inventar experiencia, certificados ni cifras. Si falta información, marcar `[COMPLETAR]` y preguntar.
- Actualizar `estado.json` al terminar la habilidad.
