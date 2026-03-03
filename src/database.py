import os
from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, Boolean
from sqlalchemy.orm import declarative_base, sessionmaker

Base = declarative_base()

class Article(Base):
    __tablename__ = 'articles'

    id = Column(Integer, primary_key=True)
    source = Column(String(255))
    title = Column(String(500))
    url = Column(String(1000), unique=True)
    published_date = Column(DateTime)
    raw_content = Column(Text)
    summary = Column(Text)
    is_relevant = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'news.db')
engine = create_engine(f'sqlite:///{DB_PATH}')
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
