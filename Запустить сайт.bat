@echo off
"%SystemRoot%\System32\chcp.com" 65001 >nul
title Сайт БГИТУ — локальный сервер
cd /d "%~dp0"
set PORT=8792
set URL=http://127.0.0.1:%PORT%/
set WHERE="%SystemRoot%\System32\where.exe"

rem ищем Python: в PATH, через py-лаунчер или в стандартных папках установки
set PY=
%WHERE% python >nul 2>nul && set PY=python
if not defined PY %WHERE% py >nul 2>nul && set PY=py
if not defined PY for /d %%D in ("%LocalAppData%\Programs\Python\Python3*") do if exist "%%D\python.exe" set PY="%%D\python.exe"
if not defined PY for /d %%D in ("%ProgramFiles%\Python3*") do if exist "%%D\python.exe" set PY="%%D\python.exe"

echo.
echo   Сайт БГИТУ: %URL%
echo   Чтобы остановить — закройте это окно.
echo.

rem браузер откроется через секунду, когда сервер уже поднимется
start "" "%SystemRoot%\System32\cmd.exe" /c ""%SystemRoot%\System32\timeout.exe" /t 1 >nul & start "" %URL%"

if defined PY (%PY% -m http.server %PORT% --bind 127.0.0.1 & goto :eof)
%WHERE% npx >nul 2>nul && (npx --yes serve -l %PORT% . & goto :eof)

echo   Не найден ни Python, ни Node.js.
echo   Установите Python с https://www.python.org/downloads/ (галочка "Add to PATH")
echo   и запустите этот файл ещё раз.
pause
