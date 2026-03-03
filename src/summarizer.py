import os
from google import genai
from .database import Article, SessionLocal
from .config import load_config
from dotenv import load_dotenv

def summarize_and_filter_unprocessed():
    """Finds articles without summaries, checks relevance, and generates summaries."""
    # Reload env vars to get the latest API key
    load_dotenv(override=True)
    api_key = os.getenv("GEMINI_API_KEY")
    
    db = SessionLocal()
    unprocessed = db.query(Article).filter(Article.summary == None).all()
    
    if not unprocessed:
        print("No new articles to summarize.")
        db.close()
        return

    if not api_key:
        print("Warning: GEMINI_API_KEY is not set. Using Mock Mode.")
        for article in unprocessed:
            article.is_relevant = True
            # Strip tags and take a snippet for mock summary
            raw_text = str(article.raw_content).replace("<", " ").replace(">", " ")[:80]
            article.summary = f"[模拟模式未配置API Key] {raw_text}..."
        db.commit()
        db.close()
        return

    config = load_config()
    keywords = config.get('keywords', [])

    print(f"Found {len(unprocessed)} articles to process.")
    
    # We use gemini-2.5-flash for fast and cost-effective text processing
    try:
        client = genai.Client(api_key=api_key)
    except Exception as e:
         print(f"Failed to initialize client. Error: {e}")
         db.close()
         return

    keywords_str = ", ".join(keywords)
    prompt_template = f"""
    我正在监控以下关键字：{keywords_str}。
    请阅读下面的文章标题和内容摘要：
    
    标题：{{title}}
    内容：{{content}}
    
    任务：
    1. 判断这篇文章是否与我的关键字高度相关。
    2. 如果相关，请用一段简练的中文总结这篇新闻的核心信息（控制在100字以内）。
    3. 如果不相关，请直接回复："无关"。
    
    只回复总结内容或"无关"，不要多余的废话。
    """

    for article in unprocessed:
        print(f"Processing: {article.title}")
        prompt = prompt_template.format(title=article.title, content=article.raw_content)
        
        try:
            response = client.models.generate_content(
                model='gemini-2.5-flash',
                contents=prompt,
            )
            result = response.text.strip()
            
            if "无关" in result and len(result) < 10:
                article.is_relevant = False
                article.summary = "Not relevant"
            else:
                article.is_relevant = True
                article.summary = result
                
        except Exception as e:
            print(f"Error processing {article.url}: {e}")
            article.summary = "Error during summarization"
            
        db.commit()
        
    db.close()
    print("Summarization complete.")
