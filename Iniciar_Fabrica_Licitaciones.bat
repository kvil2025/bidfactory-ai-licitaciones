@echo off
chcp 65001 >nul
cd /d "%~dp0"
start "" pythonw "fabrica_licitaciones_app.py"

