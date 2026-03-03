@echo off
title Erdan News - Web UI
echo Starting Streamlit Web App using uv...
cd /d "%~dp0"
uv run streamlit run app.py
pause
