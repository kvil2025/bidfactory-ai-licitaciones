"""Crea el acceso directo en el Escritorio de Windows (`Geologgia - Fábrica de Licitaciones.lnk`)
con su icono corporativo `geologgia_licitaciones.ico` apuntando al ejecutable `.exe`.
"""
from __future__ import annotations

import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def crear_acceso_directo() -> None:
    pythonw = Path(r"C:\Users\geolo\AppData\Local\Programs\Python\Python312\pythonw.exe")
    app_py = ROOT / "fabrica_licitaciones_app.py"
    ico_path = ROOT / "geologgia_licitaciones.ico"

    ps_script = f"""
$desktop = [Environment]::GetFolderPath('Desktop')
$lnkPath = Join-Path $desktop 'Geologgia - Fábrica de Licitaciones.lnk'
$wsh = New-Object -ComObject WScript.Shell
$sc = $wsh.CreateShortcut($lnkPath)
$sc.TargetPath = '{pythonw}'
$sc.Arguments = '"{app_py}"'
$sc.WorkingDirectory = '{ROOT}'
$sc.IconLocation = '{ico_path},0'
$sc.Description = 'Geologgia IA - Fábrica de Licitaciones (50 Habilidades)'
$sc.Save()
Write-Output "SHORTCUT_CREATED:$lnkPath"
"""
    res = subprocess.run(["powershell", "-NoProfile", "-Command", ps_script], check=True, text=True, capture_output=True)
    print(res.stdout.strip())


if __name__ == "__main__":
    crear_acceso_directo()
