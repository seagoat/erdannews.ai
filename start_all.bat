@echo off
title Erdan News - Start All
cd /d "%~dp0"

where uv >nul 2>nul
if %ERRORLEVEL% neq 0 (
    echo [INFO] 'uv' is not installed. Downloading and installing...
    powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
    set "PATH=%USERPROFILE%\.local\bin;%USERPROFILE%\.cargo\bin;%PATH%"
)

echo [INFO] Syncing dependencies (will download Python automatically if missing)...
call uv sync

echo [INFO] Launching Background Scheduler...
start "Erdan News - Scheduler" cmd /c "set ""PATH=%PATH%"" & uv run python -m src.scheduler & pause"

echo [INFO] Launching Web UI...
start "Erdan News - Web App" cmd /c "set ""PATH=%PATH%"" & uv run streamlit run app.py & pause"

echo Both services launched in separate windows!
pause
