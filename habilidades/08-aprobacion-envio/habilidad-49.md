# Habilidad 49 — Envío / carga de la oferta

**Fase:** VIII · Aprobación, envío y post-licitación  
**Rol responsable:** Bid Manager + Aprobador  

## Objetivo
Ingresar la oferta completa, a tiempo, y con comprobante.

## Entradas
- Paquete final
- Acta de aprobación

## Pasos
1. Verificar que existe `revision/acta_aprobacion.md`.
2. Checklist final: archivos por sobre, tamaños, nombres, garantía física (si aplica), hora de cierre.
3. El usuario sube la oferta al portal o envía el correo (la IA prepara el borrador, no envía).
4. Guardar comprobante de recepción en `envio/` y cambiar el estado a ENVIADA.

## Salida
Comprobante de envío.

## Punto de control
Enviar con al menos 24 h de margen. Los portales colapsan cerca del cierre.

## Reglas generales
- Citar siempre la fuente (documento, numeral, página) de cada dato extraído de las bases.
- No inventar experiencia, certificados ni cifras. Si falta información, marcar `[COMPLETAR]` y preguntar.
- Actualizar `estado.json` al terminar la habilidad.
