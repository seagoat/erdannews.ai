import schedule
import time
from src.scraper import fetch_rss_feeds
from src.summarizer import summarize_and_filter_unprocessed
from src.database import init_db

def job():
    print("Starting scheduled scraping job...")
    fetch_rss_feeds()
    summarize_and_filter_unprocessed()
    print("Job completed. Waiting for next run.")

def run_scheduler():
    init_db() # Ensure DB is initialized before job runs
    
    # Run once immediately on start
    job()
    
    # Schedule to run every day at 08:00 AM
    schedule.every().day.at("08:00").do(job)
    
    # Alternatively, for testing, run every 30 minutes
    # schedule.every(30).minutes.do(job)
    
    print("Scheduler is running. Press Ctrl+C to exit.")
    while True:
        schedule.run_pending()
        time.sleep(60)

if __name__ == "__main__":
    run_scheduler()
