#!/bin/bash

# Get the script directory
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$DIR"

# Check if uv is installed
if ! command -v uv &> /dev/null; then
    echo "[INFO] 'uv' is not installed. Downloading and installing..."
    curl -LsSf https://astral.sh/uv/install.sh | sh
    # Add to PATH for the current session
    export PATH="$HOME/.local/bin:$PATH"
fi

# Ensure uv is in PATH for this session
export PATH="$HOME/.local/bin:$PATH"

echo "[INFO] Syncing dependencies (will download Python automatically if missing)..."
uv sync

echo "[INFO] Running Scraper and Summarizer once for debugging..."
uv run python -c "from src.database import init_db; from src.scraper import fetch_rss_feeds; from src.summarizer import summarize_and_filter_unprocessed; init_db(); fetch_rss_feeds(); summarize_and_filter_unprocessed()"

echo ""
echo "Debug run completed. Press enter to exit."
read
