"""Ejecuta una simulación de punta a punta (Habilidades 01 a 50) para verificar
todos los scripts del Equipo de Licitaciones IA de Geologgia Ltda.
"""
from __future__ import annotations

import subprocess
import sys
from email.message import EmailMessage
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCRIPTS = ROOT / "scripts"


def run_step(args: list[str]) -> None:
    cmd = [sys.executable, *[str(a) for a in args]]
    print(">>", " ".join(cmd))
    res = subprocess.run(cmd, cwd=ROOT, check=True, text=True, capture_output=True)
    print(res.stdout.strip())


def main() -> None:
    codigo = "LIC-2026-001"
    tmp_eml = ROOT / "plantillas" / "ejemplo_invitacion_licitacion.eml"

    # Crear un correo .eml realista con adjunto de bases (TdR)
    msg = EmailMessage()
    msg["Subject"] = f"Invitación a Licitación {codigo}: Estudio Geológico-Geotécnico Túnel de Aducción y Estabilidad de Portal"
    msg["From"] = "abastecimiento@hidroenergia-austral.cl"
    msg["To"] = "licitaciones@geologgia.cl"
    msg["Date"] = "Wed, 11 Nov 2026 09:30:00 -0300"
    msg.set_content(
        "Estimados señores Geologgia Ltda.,\n\n"
        "Junto con saludar, los invitamos a participar en la licitación LIC-2026-001:\n"
        "Mandante: Hidroenergía Austral SpA\n"
        "Objeto: Estudio Geológico-Geotécnico de Detalle para Túnel de Aducción (4,2 km) y Estabilidad de Taludes del Portal de Entrada.\n"
        "Portal: SAP Ariba / Correo Oficial\n"
        "Fecha de cierre de ofertas: 2026-11-28 15:00\n\n"
        "Se adjuntan Términos de Referencia (TdR) y se solicita revisar Anexo A-3 y Anexo E-1.\n"
    )
    tdr_texto = (
        "TÉRMINOS DE REFERENCIA — LIC-2026-001\n"
        "1. ALCANCE: Mapeo geológico-geotécnico escala 1:500 (RMR89, Q de Barton, GSI), logueo de 350 m de sondajes diamantina HQ3 y recomendaciones de soporte NATM.\n"
        "2. ANEXOS EXIGIDOS: Anexo A-3 (Declaración Jurada) y Anexo E-1 (Formulario Económico en UF).\n"
    )
    msg.add_attachment(
        tdr_texto.encode("utf-8"),
        maintype="text",
        subtype="plain",
        filename="TDR_LIC-2026-001_Tunel_Aduccion.txt",
    )
    tmp_eml.write_bytes(msg.as_bytes())

    # 1. Habilidad 01: Leer correo y crear licitación
    run_step([SCRIPTS / "leer_correos.py", "--eml", tmp_eml, "--codigo", codigo])

    # 2. Habilidad 02: Extraer texto de bases e inventario de anexos
    run_step([SCRIPTS / "extraer_texto.py", codigo])

    # 3. Habilidad 09-10: Matriz de cumplimiento en Excel
    run_step([SCRIPTS / "matriz_cumplimiento.py", codigo, "--resumen"])

    # 4. Habilidad 15-16: Borrador de consultas al mandante (.eml no enviado)
    run_step([SCRIPTS / "leer_correos.py", "--borrador-consultas", codigo, "--ronda", "1"])

    # 5. Habilidad 29-34: Planilla de costos y escenarios en Excel
    run_step([SCRIPTS / "plantilla_costos.py", codigo])

    # 6. Habilidad 20-28 y 46: Propuesta técnica en Word + verificador QA
    run_step([SCRIPTS / "armar_propuesta.py", codigo, "--verificar"])

    # 7. Habilidad 47-48: Informe para Revisor Final + Acta de Aprobación
    run_step([
        SCRIPTS / "informe_aprobacion.py",
        codigo,
        "--aprobar",
        "--por",
        "Carlos Cristian Ávila Elgueta",
        "--obs",
        "Visto bueno técnico y económico otorgado. Cargar sobres en portal antes de las 15:00 del día previo al cierre.",
    ])

    # 8. Habilidad 05 y 50: Actualizar cartera general en Excel
    run_step([SCRIPTS / "cartera.py"])


if __name__ == "__main__":
    main()
