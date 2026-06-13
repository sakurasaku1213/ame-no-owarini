@echo off
rem Launch "Ame no Owari ni" (Ren'Py)
cd /d "%~dp0"
set "RENPY=C:\Users\user\Downloads\renpy-sdk\renpy.exe"
if not exist "%RENPY%" (
  echo renpy.exe not found: "%RENPY%"
  echo Edit this file and fix the RENPY path.
  pause
  exit /b 1
)
if not exist "%~dp0renpy\AmeNoOwariNi\game\script.rpy" (
  echo project not found: "%~dp0renpy\AmeNoOwariNi"
  pause
  exit /b 1
)
start "" "%RENPY%" "%~dp0renpy\AmeNoOwariNi"
exit /b 0
