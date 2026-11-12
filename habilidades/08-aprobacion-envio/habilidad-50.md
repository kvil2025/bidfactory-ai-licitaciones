# Habilidad 50 — Seguimiento de adjudicación y lecciones aprendidas

**Fase:** VIII · Aprobación, envío y post-licitación  
**Rol responsable:** Bid Manager  
**Scripts:** `cartera.py`  

## Objetivo
Aprender de cada licitación, se gane o se pierda.

## Entradas
- Acta de apertura/adjudicación
- Precios de la competencia

## Pasos
1. Registrar resultado, puntajes y precios de todos los oferentes (si son públicos).
2. Si se pierde: solicitar retroalimentación al mandante.
3. Escribir `envio/lecciones_aprendidas.md`: qué funcionó, qué no, qué cambiar.
4. Actualizar `base_conocimiento/` (tarifas, experiencia, precios de competencia) y la cartera.

## Salida
Lecciones aprendidas + base de conocimiento actualizada.

## Reglas generales
- Citar siempre la fuente (documento, numeral, página) de cada dato extraído de las bases.
- No inventar experiencia, certificados ni cifras. Si falta información, marcar `[COMPLETAR]` y preguntar.
- Actualizar `estado.json` al terminar la habilidad.
