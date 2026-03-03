@echo off
title Erdan News - Web UI
cd /d "%~dp0"

where uv >nul 2>nul
if %ERRORLEVEL% neq 0 (
    echo [INFO] 'uv' is not installed. Downloading and installing...
    powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
    set "PATH=%USERPROFILE%\.local\bin;%USERPROFILE%\.cargo\bin;%PATH%"
)

echo [INFO] Syncing dependencies (will download Python automatically if missing)...
call uv sync

echo [INFO] Starting Streamlit Web App...
uv run streamlit run app.py
pause
