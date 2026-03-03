@echo off
title Erdan News - Debug Scraper
cd /d "%~dp0"

where uv >nul 2>nul
if %ERRORLEVEL% neq 0 (
    echo [INFO] 'uv' is not installed. Downloading and installing...
    powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
    set "PATH=%USERPROFILE%\.local\bin;%USERPROFILE%\.cargo\bin;%PATH%"
)

echo [INFO] Syncing dependencies (will download Python automatically if missing)...
call uv sync

echo [INFO] Running Scraper and Summarizer once for debugging...
uv run python -c "from src.database import init_db; from src.scraper import fetch_rss_feeds; from src.summarizer import summarize_and_filter_unprocessed; init_db(); fetch_rss_feeds(); summarize_and_filter_unprocessed()"

echo.
echo Debug run completed.
pause
