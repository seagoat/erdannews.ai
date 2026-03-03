@echo off
title Erdan News - Start All
echo Starting Erdan News System...
cd /d "%~dp0"

echo Launching Background Scheduler...
start "Erdan News - Scheduler" cmd /c "uv run python -m src.scheduler & pause"

echo Launching Web UI...
start "Erdan News - Web App" cmd /c "uv run streamlit run app.py & pause"

echo Both services launched in separate windows!
pause
