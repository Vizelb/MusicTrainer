@echo off
rem ---------------------------------------------------------------
rem  MusicTrainer - build Android APK via Docker + buildozer
rem
rem  Usage:
rem      build_android.bat            build debug APK (incremental)
rem      build_android.bat clean      wipe the build cache first
rem
rem  Requires Docker Desktop to be running.
rem  First build downloads the Android SDK/NDK (~3 GB) and takes
rem  40-90 minutes. Later builds reuse the .buildozer cache and are
rem  much faster - that is why this script does NOT delete it.
rem
rem  NOTE: keep this file ASCII-only. cmd.exe parses .bat byte by
rem  byte, so non-ASCII characters here corrupt its command parsing.
rem ---------------------------------------------------------------

chcp 65001 >nul
cd /d "%~dp0"

where docker >nul 2>&1
if errorlevel 1 (
    echo.
    echo [ERROR] Docker CLI not found.
    echo Install Docker Desktop: https://www.docker.com/products/docker-desktop/
    echo.
    pause
    exit /b 1
)

docker info >nul 2>&1
if errorlevel 1 (
    echo.
    echo [ERROR] Docker engine is not running.
    echo Start Docker Desktop and wait until it reports "Engine running".
    echo.
    pause
    exit /b 1
)

if /i "%~1"=="clean" (
    echo Wiping build cache...
    if exist ".buildozer" rmdir /s /q ".buildozer"
    if exist "bin" rmdir /s /q "bin"
    echo Cache wiped. The next build will be a full one.
    echo.
)

rem BuildKit resolves DNS through its own network path, which breaks
rem when a VPN tunnel is active: "resolving host registry-1.docker.io:
rem no such host", while a plain "docker pull" works fine. The legacy
rem builder uses the daemon network path, so force it.
set DOCKER_BUILDKIT=0

echo ===============================================================
echo  Step 1/2: building the Docker image
echo ===============================================================
docker build -t musictrainer-builder .
if errorlevel 1 (
    echo.
    echo [ERROR] Docker image build failed.
    pause
    exit /b 1
)

echo.
echo ===============================================================
echo  Step 2/2: building the APK
echo  This takes a while. Full log goes to build.log
echo ===============================================================

docker run --rm -v "%cd%:/app" -w /app --user root ^
    -e USE_X11=0 -e KIVY_GL_BACKEND=sdl2 -e KIVY_NO_X11=1 -e KIVY_USE_X11=0 ^
    musictrainer-builder bash -c "chown -R builder:builder /app && su builder -c 'cd /app && buildozer android debug --verbose 2>&1 | tee build.log'"

if errorlevel 1 (
    echo.
    echo [ERROR] APK build failed. Check build.log for the reason.
    echo.
    pause
    exit /b 1
)

echo.
echo ===============================================================
echo  Done. APK is in the bin\ folder:
echo ===============================================================
dir /b bin\*.apk 2>nul
if errorlevel 1 (
    echo [WARNING] No .apk found in bin\ - check build.log
    pause
    exit /b 1
)

echo.
echo Install it on a connected phone with:
echo     adb install -r bin\<name>.apk
echo.
pause
