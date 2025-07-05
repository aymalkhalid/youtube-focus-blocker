@echo off
title YouTube Stopper - Build Executable
echo.
echo ================================================
echo        YouTube Stopper Executable Builder
echo ================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorLevel% neq 0 (
    echo ❌ Python is not installed or not in PATH
    echo Please install Python 3.8+ and try again
    pause
    exit /b 1
)

echo ✅ Python is installed

REM Check if we're in the right directory
if not exist "app.py" (
    echo ❌ Error: app.py not found
    echo Make sure you're running this from the YouTube Stopper project folder
    pause
    exit /b 1
)

echo ✅ Found app.py

REM Install/upgrade dependencies
echo.
echo 📦 Installing dependencies...
pip install -r requirements.txt

REM Clean old builds
echo.
echo 🧹 Cleaning old builds...
if exist "build" rmdir /s /q "build"
if exist "dist" rmdir /s /q "dist"
if exist "*.spec" del "*.spec"

REM Build executable
echo.
echo 🔧 Building executable...
echo This may take a few minutes...

pyinstaller --onefile ^
    --windowed ^
    --name "YouTubeStopper" ^
    --uac-admin ^
    --hidden-import tkinter ^
    --hidden-import tkinter.messagebox ^
    --hidden-import motivation_widget ^
    --hidden-import pomodoro_widget ^
    --hidden-import youtube_stopper ^
    --exclude-module matplotlib ^
    --exclude-module pygame ^
    --exclude-module playsound ^
    --exclude-module numpy ^
    app.py

if %errorLevel% neq 0 (
    echo ❌ Build failed
    pause
    exit /b 1
)

REM Check if executable was created
if not exist "dist\YouTubeStopper.exe" (
    echo ❌ Executable was not created
    pause
    exit /b 1
)

REM Create launcher batch file
echo.
echo 📝 Creating launcher...
echo @echo off > "dist\launcher.bat"
echo title YouTube Stopper >> "dist\launcher.bat"
echo echo Starting YouTube Stopper... >> "dist\launcher.bat"
echo powershell -Command "Start-Process -FilePath '%%~dp0YouTubeStopper.exe' -Verb RunAs" >> "dist\launcher.bat"

REM Success message
echo.
echo ================================================
echo ✅ Build completed successfully!
echo ================================================
echo.
echo 📁 Your executable is located at:
echo    dist\YouTubeStopper.exe
echo.
echo 🚀 To run:
echo    - Use dist\launcher.bat (recommended)
echo    - Or right-click YouTubeStopper.exe → "Run as Administrator"
echo.
echo 📦 Files created:
for %%f in (dist\*) do echo    - %%f

echo.
echo 💡 Tip: You can distribute the entire 'dist' folder
pause
