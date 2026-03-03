import feedparser
from datetime import datetime
from .database import Article, SessionLocal
from .config import load_config

def fetch_rss_feeds():
    """Fetches articles from RSS feeds and saves new ones to DB."""
    config = load_config()
    feeds = config.get('feeds', [])
    
    db = SessionLocal()
    new_articles_count = 0
    
    for feed_info in feeds:
        print(f"Fetching {feed_info['name']}...")
        try:
            feed = feedparser.parse(feed_info['url'])
        except Exception as e:
            print(f"Error parsing {feed_info['url']}: {e}")
            continue
        
        for entry in feed.entries:
            # Check if URL already exists
            existing = db.query(Article).filter(Article.url == entry.link).first()
            if existing:
                continue
            
            # Extract content (rss often has description or summary)
            content = entry.get('description', '') or entry.get('summary', '')
            
            # Parse dates
            pub_date = datetime.now()
            if hasattr(entry, 'published_parsed') and entry.published_parsed:
                pub_date = datetime(*entry.published_parsed[:6])
                
            article = Article(
                source=feed_info['name'],
                title=entry.title,
                url=entry.link,
                published_date=pub_date,
                raw_content=content
            )
            db.add(article)
            new_articles_count += 1
            
    try:
        db.commit()
        print(f"Scraped {new_articles_count} new articles.")
    except Exception as e:
        db.rollback()
        print(f"Error saving to DB: {e}")
    finally:
        db.close()
