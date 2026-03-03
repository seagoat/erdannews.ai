@echo off
title Erdan News - Debug Scraper
echo Running Scraper and Summarizer once for debugging...
cd /d "%~dp0"
uv run python -c "from src.database import init_db; from src.scraper import fetch_rss_feeds; from src.summarizer import summarize_and_filter_unprocessed; init_db(); fetch_rss_feeds(); summarize_and_filter_unprocessed()"
echo.
echo Debug run completed.
pause
