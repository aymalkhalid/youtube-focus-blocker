@echo off
title YouTube Stopper - Productivity App

echo.
echo ==========================================
echo    🎯 YouTube Stopper - Starting...
echo ==========================================
echo.
echo 📌 This app helps you stay focused by blocking YouTube distractions
echo 🔒 Administrator privileges are required for blocking functionality
echo.

REM Try to run with the virtual environment Python first
if exist ".venv\Scripts\python.exe" (
    echo 🐍 Using virtual environment Python...
    ".venv\Scripts\python.exe" run.py
) else (
    echo 🐍 Using system Python...
    python run.py
)

echo.
echo 👋 YouTube Stopper has closed.
pause
