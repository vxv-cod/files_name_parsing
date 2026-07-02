call %CD%\venv\Scripts\activate.bat

pyinstaller -w -F -i "logo.ico" app.py

@REM xcopy %CD%\*.ico %CD%\dist /H /Y /C /R

@REM xcopy %CD%\dist %CD%\ConsoleApp\ /H /Y /C /R