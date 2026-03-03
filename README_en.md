# 📰 Erdan News Aggregation System

**Erdan News Aggregation System** is a lightweight, automated, and AI-driven news and information aggregation tool. It routinely scrapes content from your specified RSS feeds and leverages Google's Gemini Large Language Model to filter out irrelevant noise based on your target keywords. Finally, it provides you with concise Chinese summaries (under 100 words) of the most relevant news.

## ✨ Core Features

*   **🤖 AI Smart Filtering & Summarization**: Integrates with the Gemini API to understand long articles, automatically filter out irrelevant info, and summarize the core message for you.
*   **🌐 Dynamic Configuration**: Features an intuitive Web UI where you can update your tracked keywords (e.g., "AI", "Open Source") and target RSS feeds (e.g., V2EX, HackerNews) on the fly. Changes take effect immediately.
*   **⏰ Automated Scheduling**: The background scheduler runs quietly, automatically collecting and summarizing your daily briefing.
*   **🛠️ Mock Mode**: If an API Key is not configured, the system automatically falls back to a mock mode, displaying the raw scraped content directly, making initial setup and debugging a breeze.
*   **📦 Minimalist Deployment**: Uses `uv` for lightning-fast package management and local SQLite for storage. No complex infrastructure required.

## 🚀 Quick Start

This project uses `uv` to manage the virtual environment and dependencies.

### 1. Install Dependencies
```bash
# Ensure you have uv installed (https://github.com/astral-sh/uv)
uv sync
```

### 2. Start the System
We provide several convenient batch scripts for Windows users:

*   **`start_all.bat` (Recommended)**: One-click start for both the "Background Scheduler" and the "Web UI".
*   **`debug_scraper.bat`**: Manually force a single run of the scraper and AI summarizer (useful for debugging).
*   **`start_web.bat`**: Start the Web UI only.
*   **`start_scheduler.bat`**: Start the background scheduler only.

### 3. Configure the System (via Web UI)
1. Run `start_all.bat`, and your browser will automatically open the web app (usually at `http://localhost:8501`).
2. Navigate to the **"⚙️ 系统配置" (System Configuration)** tab.
3. Enter your `GEMINI_API_KEY` in the API Key section (leave blank to experience the mock mode).
4. Customize your tracked keywords and RSS sources, then click save.

## 📂 Project Structure

*   `app.py`: The Streamlit Web frontend UI.
*   `src/scraper.py`: Scraper module responsible for fetching raw articles from RSS feeds.
*   `src/summarizer.py`: Core logic for interacting with Gemini, determining relevance, and generating summaries.
*   `src/scheduler.py`: Background task scheduler.
*   `src/database.py`: SQLite database schema and connection setup.
*   `src/config.py`: Logic for reading and saving dynamic user configurations (keywords, feeds).

## 🤝 Customization
If you want to target specific websites that do not offer RSS feeds, you can easily modify `src/scraper.py` and introduce custom scraping logic using libraries like `BeautifulSoup` or `Playwright`.
