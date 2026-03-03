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

# Launch processes based on OS
if [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS: Launch Scheduler in a new window and Web UI in the current one
    echo "[INFO] Launching Background Scheduler in a new Terminal window..."
    osascript -e "tell application \"Terminal\" to do script \"cd '$DIR' && export PATH='$PATH' && uv run python -m src.scheduler\""
    
    echo "[INFO] Launching Web UI..."
    uv run streamlit run app.py
else
    # Linux/Other: Launch Scheduler in background and Web UI in foreground
    echo "[INFO] Launching Background Scheduler..."
    uv run python -m src.scheduler > scheduler.log 2>&1 &
    
    echo "[INFO] Launching Web UI..."
    uv run streamlit run app.py
fi
