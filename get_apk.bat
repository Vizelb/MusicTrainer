@echo off
rem ---------------------------------------------------------------
rem  MusicTrainer - download the APK built by GitHub Actions
rem
rem  Usage:
rem      get_apk.bat            download latest successful build to bin\
rem      get_apk.bat install    download, then install on a connected phone
rem
rem  Requires GitHub CLI (gh) authenticated via "gh auth login".
rem  The APK is NOT produced locally: GitHub builds it on its own server
rem  and keeps it as a build artifact for 90 days. This script fetches it.
rem
rem  NOTE: keep this file ASCII-only. cmd.exe parses .bat byte by byte,
rem  so non-ASCII characters here corrupt its command parsing.
rem
rem  NOTE: tool directories are prepended to PATH instead of calling the
rem  exe by quoted full path - a quoted path breaks inside for /f `...`,
rem  which fails as: 'C:\Program' is not recognized as a command.
rem ---------------------------------------------------------------

chcp 65001 >nul
cd /d "%~dp0"

set REPO=Vizelb/MusicTrainer
set "PATH=%ProgramFiles%\GitHub CLI;%LOCALAPPDATA%\Android\Sdk\platform-tools;%PATH%"

where gh >nul 2>&1
if errorlevel 1 (
    echo.
    echo [ERROR] GitHub CLI not found.
    echo Install it, then run: gh auth login
    echo.
    pause
    exit /b 1
)

gh auth status >nul 2>&1
if errorlevel 1 (
    echo.
    echo [ERROR] GitHub CLI is not authenticated.
    echo Run this in your own terminal:  gh auth login
    echo.
    pause
    exit /b 1
)

echo Looking up the latest successful build...
set RUN_ID=
for /f "usebackq delims=" %%i in (`gh run list --repo %REPO% --workflow "Build Android APK" --status success --limit 1 --json databaseId --jq ".[0].databaseId"`) do set RUN_ID=%%i

if "%RUN_ID%"=="" (
    echo.
    echo [ERROR] No successful build found.
    echo Check builds with:  gh run list --repo %REPO%
    echo.
    pause
    exit /b 1
)

echo Found build %RUN_ID%. Downloading...

if not exist "bin" mkdir "bin"
del /q "bin\*.apk" 2>nul

rem The connection drops on slow links, so retry a few times.
set ATTEMPT=0
:retry
set /a ATTEMPT+=1
gh run download %RUN_ID% --repo %REPO% -n musictrainer-apk --dir "bin" >nul 2>&1
dir /b "bin\*.apk" >nul 2>&1
if not errorlevel 1 goto downloaded
if %ATTEMPT% GEQ 4 (
    echo.
    echo [ERROR] Download failed after %ATTEMPT% attempts.
    echo Download it by hand from:
    echo     https://github.com/%REPO%/actions/runs/%RUN_ID%
    echo.
    pause
    exit /b 1
)
echo   attempt %ATTEMPT% failed, retrying...
rem ping instead of timeout: timeout refuses to run when stdin is redirected
ping -n 6 127.0.0.1 >nul
goto retry

:downloaded
echo.
echo Done. APK is in bin\:
for %%f in (bin\*.apk) do echo     %%~nxf  (%%~zf bytes)

if /i not "%~1"=="install" (
    echo.
    echo To install it on a connected phone, run:  get_apk.bat install
    echo.
    pause
    exit /b 0
)

rem ---------------- install on device ----------------
where adb >nul 2>&1
if errorlevel 1 (
    echo.
    echo [ERROR] adb not found. Install Android SDK platform-tools.
    echo.
    pause
    exit /b 1
)

echo.
echo Connected devices:
adb devices

for %%f in (bin\*.apk) do (
    echo.
    echo Installing %%~nxf ...
    adb install -r "%%f"
)

echo.
echo If the phone is not listed above, enable USB debugging on it.
echo To watch the app log:  adb logcat -s python
echo.
pause
