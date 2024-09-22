# import json
import json
from sqlalchemy import (
    DateTime,
    ForeignKey,
    create_engine,
    Column,
    Integer,
    String,
    Text,
)
import os
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import feedparser
import requests
from datetime import datetime
from sqlalchemy.orm import relationship, sessionmaker

os.makedirs(os.path.expanduser("~/data"), exist_ok=True)
os.makedirs("./data", exist_ok=True)
Base = declarative_base()


class RSSSource(Base):
    __tablename__ = "rss_source"
    id = Column(Integer, primary_key=True)
    url = Column(String, unique=True)
    link = Column(String, unique=True)
    name = Column(Text)
    avatar_url = Column(Text)
    created = Column(DateTime)
    creator = Column(String)
    creator_url = Column(String)
    num_subed = Column(Integer, default=0)
    type = Column(Integer, default=0)
    cate = Column(String)

    def to_dict(self):
        return {
            "id": self.id,
            "url": self.url,
            "link": self.link,
            "name": self.name,
            "created": self.created.isoformat() if self.created else None,
            "creator": self.creator,
            "creator_url": self.creator_url,
            "num_subed": self.num_subed,
            "type": self.type,
            "cate": self.cate,
        }

    def to_json(self):
        return json.dumps(self.to_dict(), indent=2, ensure_ascii=False)


class RSSFeed(Base):
    __tablename__ = "rss_feeds"
    id = Column(Integer, autoincrement=True)
    url = Column(String, unique=True, primary_key=True)
    uuid = Column(String)
    content = Column(Text)
    title = Column(String)
    hero_img_url = Column(String)
    published = Column(DateTime)
    created = Column(DateTime)
    author = Column(String)
    source_name = Column(String)
    source_url = Column(String)
    source_avatar_url = Column(String)
    summary = Column(Text)
    ai_summary = Column(Text)  # Field for AI-generated summary
    tags = Column(Text)  # Field for AI-generated labels
    num_looked = Column(
        Integer, default=0
    )  # Number of times the feed has been looked at
    comments = relationship("Comment", back_populates="feed")

    def to_dict(self):
        return {
            "id": self.id,
            "uuid": self.uuid,
            "url": self.url,
            "content": self.content,
            "title": self.title,
            "published": self.published.isoformat() if self.published else None,
            "created": self.created.isoformat() if self.created else None,
            "author": self.author,
            "source_name": self.source_name,
            "source_url": self.source_url,
            "source_avatar_url": self.source_avatar_url,
            "summary": self.summary,
            "ai_summary": self.ai_summary,
            "tags": self.tags,
            "num_looked": self.num_looked,
            "comments": self.comments,
            "hero_img_url": self.hero_img_url,
        }

    def to_json(self):
        return json.dumps(self.to_dict(), indent=2, ensure_ascii=False)


class Comment(Base):
    __tablename__ = "comments"
    id = Column(Integer, primary_key=True)
    feed_id = Column(Integer, ForeignKey("rss_feeds.id"))
    user_name = Column(String)
    user_avatar_url = Column(String)
    comment_time = Column(DateTime, default=datetime.utcnow)
    comment_content = Column(Text)
    feed = relationship("RSSFeed", back_populates="comments")


# sql_p = os.path.join(os.path.expanduser("~/data"), "rss_feeds.db")
sql_p = "data/rss_feeds.db"
engine = create_engine(f"sqlite:///{sql_p}")
print(f"sqlite path: {sql_p}")
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()
