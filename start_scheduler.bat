@echo off
title Erdan News - Background Scheduler
cd /d "%~dp0"

where uv >nul 2>nul
if %ERRORLEVEL% neq 0 (
    echo [INFO] 'uv' is not installed. Downloading and installing...
    powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
    set "PATH=%USERPROFILE%\.local\bin;%USERPROFILE%\.cargo\bin;%PATH%"
)

echo [INFO] Syncing dependencies (will download Python automatically if missing)...
call uv sync

echo [INFO] Starting Background Scraper Scheduler...
uv run python -m src.scheduler
pause
