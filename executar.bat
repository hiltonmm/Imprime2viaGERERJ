@echo off
cd /d "%~dp0"
call .venv\Scripts\activate.bat
python imprimir_grerjs.py
pause