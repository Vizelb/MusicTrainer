@echo off
rem ---------------------------------------------------------------
rem  MusicTrainer launcher
rem
rem  Just double-click this file in Explorer.
rem  It cd's to the project root on purpose: the app stores settings
rem  and statistics relative to the current working directory.
rem
rem  NOTE: keep this file ASCII-only. cmd.exe parses .bat byte by
rem  byte, so non-ASCII characters here corrupt its command parsing.
rem  Russian output of the app itself is fine - that is what the
rem  chcp 65001 below is for.
rem ---------------------------------------------------------------

chcp 65001 >nul
cd /d "%~dp0"

rem UTF-8 mode: without it print() with emoji crashes on a cp1251 console
set PYTHONUTF8=1
set PYTHONIOENCODING=utf-8

if not exist ".venv\Scripts\python.exe" (
    echo.
    echo [ERROR] Virtual environment .venv not found.
    echo.
    echo Create it with two commands:
    echo     python -m venv .venv
    echo     .venv\Scripts\pip install -r requirements.txt
    echo.
    pause
    exit /b 1
)

if not exist "src\main.py" (
    echo.
    echo [ERROR] src\main.py not found.
    echo Run this script from the MusicTrainer project root.
    echo.
    pause
    exit /b 1
)

echo Starting MusicTrainer...
echo.

".venv\Scripts\python.exe" "src\main.py"
set EXITCODE=%errorlevel%

if not "%EXITCODE%"=="0" (
    echo.
    echo [ERROR] Application exited with code %EXITCODE%.
    echo See the output above and %%USERPROFILE%%\.kivy\logs\
    echo.
    pause
)

exit /b %EXITCODE%
