import streamlit as st
import pandas as pd
import os
from dotenv import load_dotenv, set_key
from sqlalchemy import desc, func
from src.database import SessionLocal, Article, init_db
from src.config import load_config, save_config

# Initialize database tables if they don't exist
init_db()

# Ensure .env exists
ENV_PATH = os.path.join(os.path.dirname(__file__), '.env')
if not os.path.exists(ENV_PATH):
    with open(ENV_PATH, 'w') as f:
        f.write("")

load_dotenv(ENV_PATH)

st.set_page_config(page_title="二蛋信息采集系统", page_icon="📰", layout="wide")

# Remove the problematic custom CSS for sticky tabs as we are moving navigation to the sidebar
st.markdown("""
    <style>
        /* Hide the default Streamlit top header */
        header[data-testid="stHeader"] {
            display: none !important;
        }

        /* Adjust top padding */
        .block-container {
            padding-top: 2rem !important;
        }
    </style>
""", unsafe_allow_html=True)

config = load_config()
KEYWORDS = config.get("keywords", [])
FEEDS = config.get("feeds", [])

st.title("📰 二蛋信息采集系统")

# Fetch data
@st.cache_data(ttl=60)
def load_data():
    db = SessionLocal()
    try:
        articles = db.query(Article)\
            .filter(Article.is_relevant == True)\
            .filter(Article.summary != 'Not relevant')\
            .filter(Article.summary != None)\
            .order_by(desc(Article.published_date))\
            .limit(100)\
            .all()
        
        data = []
        for a in articles:
            pub_date_str = a.published_date.strftime("%Y-%m-%d %H:%M") if a.published_date else "未知时间"
            data.append({
                "Source": a.source,
                "Title": a.title,
                "Summary": a.summary,
                "RawContent": a.raw_content,
                "Date": pub_date_str,
                "URL": a.url
            })
        return pd.DataFrame(data)
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return pd.DataFrame()
    finally:
        db.close()

@st.cache_data(ttl=60)
def load_stats():
    db = SessionLocal()
    try:
        total = db.query(Article).count()
        relevant = db.query(Article).filter(Article.is_relevant == True).count()
        last_record = db.query(Article).order_by(desc(Article.created_at)).first()
        last_time = last_record.created_at.strftime("%Y-%m-%d %H:%M:%S") if last_record and last_record.created_at else "无记录"
        
        history = db.query(
            Article.source, 
            func.count(Article.id).label('count'),
            func.max(Article.created_at).label('last_time')
        ).group_by(Article.source).all()
        
        history_data = []
        for h in history:
            history_data.append({
                "采集源": h.source, 
                "已采集总数": h.count, 
                "最后采集时间": h.last_time.strftime("%Y-%m-%d %H:%M:%S") if h.last_time else "-"
            })
        
        return total, relevant, last_time, pd.DataFrame(history_data)
    except Exception as e:
        st.error(f"Error loading stats: {e}")
        return 0, 0, "Error", pd.DataFrame()
    finally:
        db.close()

# Sidebar Navigation
st.sidebar.title("🧭 导航菜单")
page = st.sidebar.radio("选择功能视图", ["🗞️ 最新资讯", "📊 采集状态与历史", "⚙️ 系统配置"])
st.sidebar.divider()

if page == "🗞️ 最新资讯":
    col_title, col_btn = st.columns([4, 1])
    with col_btn:
        if st.button("🔄 手动刷新数据"):
            load_data.clear()
            st.rerun()

    df = load_data()

    if df.empty:
        st.info("还没有采集到与关键字相关的最新内容，或者爬虫尚未运行。请稍后刷新。")
    else:
        # Move filters into an expander or keep them in sidebar if it's the News page
        st.sidebar.header("🎯 资讯过滤选项")
        sources = df['Source'].unique().tolist()
        selected_sources = st.sidebar.multiselect("选择信息源", sources, default=sources)
        
        selected_keywords = st.sidebar.multiselect("包含关键字 (文本匹配)", KEYWORDS, default=[])
        
        group_by = st.sidebar.radio("分组方式", ["按日期", "按信息源"])
        
        filtered_df = df[df['Source'].isin(selected_sources)]
        
        if selected_keywords:
            keyword_mask = filtered_df.apply(lambda row: any(
                k.lower() in str(row.get('RawContent', '')).lower() or 
                k.lower() in str(row.get('Summary', '')).lower() or 
                k.lower() in str(row.get('Title', '')).lower() 
                for k in selected_keywords
            ), axis=1)
            filtered_df = filtered_df[keyword_mask]
        
        st.write(f"共为您精选出 **{len(filtered_df)}** 条相关资讯：")
        
        if filtered_df.empty:
            st.warning("没有找到匹配条件的资讯，请尝试放宽过滤选项。")
        else:
            if group_by == "按日期":
                current_date = None
                for idx, row in filtered_df.iterrows():
                    row_date = row['Date'].split(' ')[0] if ' ' in row['Date'] else row['Date']
                    
                    if current_date != row_date:
                        current_date = row_date
                        st.markdown(f"## 📅 {current_date}")
                        st.divider()

                    with st.container():
                        st.subheader(f"{row['Title']}")
                        col1, col2 = st.columns([3, 1])
                        with col1:
                            st.markdown(f"> {row['Summary']}")
                            with st.expander("查看原始抓取内容"):
                                st.text(row.get('RawContent', '无原始内容'))
                            st.markdown(f"[🔗 阅读全文]({row['URL']})")
                        with col2:
                            time_str = row['Date'].split(' ')[1] if ' ' in row['Date'] else row['Date']
                            st.caption(f"🕒 {time_str}")
                            st.caption(f"📍 {row['Source']}")
                        st.markdown("<br>", unsafe_allow_html=True)
            else:
                sorted_df = filtered_df.sort_values(by=['Source', 'Date'], ascending=[True, False])
                current_source = None
                for idx, row in sorted_df.iterrows():
                    if current_source != row['Source']:
                        current_source = row['Source']
                        st.markdown(f"## 📍 {current_source}")
                        st.divider()

                    with st.container():
                        st.subheader(f"{row['Title']}")
                        col1, col2 = st.columns([3, 1])
                        with col1:
                            st.markdown(f"> {row['Summary']}")
                            with st.expander("查看原始抓取内容"):
                                st.text(row.get('RawContent', '无原始内容'))
                            st.markdown(f"[🔗 阅读全文]({row['URL']})")
                        with col2:
                            st.caption(f"📅 {row['Date']}")
                        st.markdown("<br>", unsafe_allow_html=True)

elif page == "📊 采集状态与历史":
    st.header("系统状态与采集历史")
    
    total_articles, relevant_articles, last_scrape_time, df_history = load_stats()
    
    col1, col2, col3 = st.columns(3)
    col1.metric("总抓取文章数", total_articles)
    col2.metric("AI筛选相关文章数", relevant_articles)
    col3.metric("最后采集时间", last_scrape_time)
    
    st.markdown("### 📊 各站点采集明细")
    if not df_history.empty:
        st.dataframe(df_history, width='stretch', hide_index=True)
    else:
        st.info("暂无采集历史记录。")

elif page == "⚙️ 系统配置":
    st.header("系统动态配置")
    st.markdown("在这里修改的所有配置将立即生效，后台调度器会自动使用最新配置。")
    
    st.subheader("🔑 API Key 配置")
    current_key = os.getenv("GEMINI_API_KEY", "")
    new_key = st.text_input("Gemini API Key", value=current_key, type="password", help="在此输入您的 Gemini API 密钥 (存于 .env)。")
    if st.button("保存 API Key"):
        set_key(ENV_PATH, "GEMINI_API_KEY", new_key)
        os.environ["GEMINI_API_KEY"] = new_key
        st.success("API Key 已成功保存至 .env 文件！下次总结任务将使用新 Key。")
    
    st.divider()
    
    col_kw, col_sites = st.columns(2)
    
    with col_kw:
        st.subheader("🎯 追踪关键字")
        st.caption("每行输入一个关键字，AI 会判断新闻是否命中这些词。")
        keywords_text = st.text_area("关键字列表", value="\n".join(KEYWORDS), height=200)
        if st.button("保存关键字"):
            new_keywords = [k.strip() for k in keywords_text.split("\n") if k.strip()]
            config["keywords"] = new_keywords
            save_config(config)
            st.success("关键字已更新并写入 config.json！")
            st.rerun()

    with col_sites:
        st.subheader("🌐 采集源 (RSS)")
        st.caption("格式：名称|RSS地址，每行一个。如：V2EX|https://www.v2ex.com/index.xml")
        
        feeds_text_lines = []
        for f in FEEDS:
            feeds_text_lines.append(f"{f['name']}|{f['url']}")
            
        feeds_text = st.text_area("RSS 数据源", value="\n".join(feeds_text_lines), height=200)
        if st.button("保存采集源"):
            new_feeds = []
            for line in feeds_text.split("\n"):
                if "|" in line:
                    name, url = line.split("|", 1)
                    new_feeds.append({"name": name.strip(), "url": url.strip()})
            config["feeds"] = new_feeds
            save_config(config)
            st.success("采集源已更新并写入 config.json！")
            st.rerun()

st.sidebar.markdown("---")
st.sidebar.caption("提示: 爬虫与总结任务在后台通过 src/scheduler.py 定时运行。")
