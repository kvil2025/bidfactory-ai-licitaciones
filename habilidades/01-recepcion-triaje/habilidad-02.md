# Habilidad 02 — Descarga y orden de bases y anexos

**Fase:** I · Recepción y triaje  
**Rol responsable:** Bid Manager  
**Scripts:** `extraer_texto.py`  

## Objetivo
Reunir todos los documentos de la licitación en una estructura estándar y convertirlos a texto analizable.

## Entradas
- Adjuntos del correo
- Links a portales (Mercado Público, SAP Ariba, Coupa, portal del mandante)

## Pasos
1. Mover los documentos a `bases/` con nombres normalizados: `BAG_`, `BAE_`, `TDR_`, `ANEXO_NN_`, `PLANO_`, `ADENDA_NN_`.
2. Si hay documentos solo en portal, listar en `bases/PENDIENTES.md` lo que el usuario debe descargar manualmente (nunca usar credenciales sin autorización).
3. Ejecutar `python scripts/extraer_texto.py <CODIGO>` para generar `analisis/texto/*.txt`.
4. Verificar que no falten anexos citados en las bases (buscar 'Anexo N°' en el texto y cruzar con los archivos).

## Salida
`licitaciones/<CODIGO>/bases/` ordenado + `analisis/texto/` + lista de faltantes.

## Reglas generales
- Citar siempre la fuente (documento, numeral, página) de cada dato extraído de las bases.
- No inventar experiencia, certificados ni cifras. Si falta información, marcar `[COMPLETAR]` y preguntar.
- Actualizar `estado.json` al terminar la habilidad.
