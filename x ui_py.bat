@echo off
chcp 65001
set "SCRIPT_DIR=%~dp0"

call "%SCRIPT_DIR%venv\Scripts\activate.bat"

"%SCRIPT_DIR%venv\Scripts\python.exe" -m PyQt5.uic.pyuic -x "%SCRIPT_DIR%okno.ui" -o "%SCRIPT_DIR%okno_ui.py"