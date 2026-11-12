# Habilidad 01 — Lectura del correo de invitación

**Fase:** I · Recepción y triaje  
**Rol responsable:** Bid Manager  
**Scripts:** `leer_correos.py, nueva_licitacion.py`  

## Objetivo
Detectar correos de invitación, bases, aclaraciones o adendas, y crear la carpeta de la licitación.

## Entradas
- Bandeja Gmail (IMAP)
- Correos reenviados o descargados (.eml)

## Pasos
1. Ejecutar `python scripts/leer_correos.py --dias 7` (o `--eml archivo.eml`).
2. Clasificar cada correo: invitación nueva / consulta-respuesta / adenda / recordatorio / adjudicación.
3. Identificar mandante, código o ID de licitación, nombre del proyecto, plazos mencionados y contacto.
4. Si es nueva, crear la estructura con `python scripts/nueva_licitacion.py <CODIGO> "<Nombre>" "<Mandante>"`.
5. Si corresponde a una licitación existente, guardarlo en `correo/` y avisar al Bid Manager qué cambió.

## Salida
`licitaciones/<CODIGO>/correo/` con .eml + adjuntos y entrada en `estado.json`.

## Reglas generales
- Citar siempre la fuente (documento, numeral, página) de cada dato extraído de las bases.
- No inventar experiencia, certificados ni cifras. Si falta información, marcar `[COMPLETAR]` y preguntar.
- Actualizar `estado.json` al terminar la habilidad.
