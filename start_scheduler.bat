@echo off
title Erdan News - Background Scheduler
echo Starting Background Scraper Scheduler using uv...
cd /d "%~dp0"
uv run python -m src.scheduler
pause
