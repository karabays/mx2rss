import datetime

from sqlalchemy import create_engine, Boolean, Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship, Session

from fastapi_rss import RSSFeed, RSSResponse, Item, Category, CategoryAttrs, GUID

import app.models as models
import app.config as config
from app.log import logger



SQLALCHEMY_DATABASE_URL = "sqlite:///./app/mx2rss.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

db = SessionLocal()

Base = declarative_base()

settings = config.settings

class Feed(Base):
    __tablename__ = "feeds"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    email_id = Column(String, unique=True, index=True)
    domain = Column(String, index=True)
    url = Column(String)
    last_build_date = Column(DateTime, index=True)
    items = relationship("FeedItem", back_populates="feed")

class FeedItem(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, index=True)
    author = Column(String, index=True)
    pub_date = Column(DateTime, index=True)
    guid = Column(String, index=True)
    feed_id = Column(Integer, ForeignKey("feeds.id"))
    feed = relationship("Feed", back_populates="items")


def get_feed_by_email(email: str):
    return db.query(Feed).filter(Feed.email == email).first()


def get_feed_by_email_id(email_id: str):
    return db.query(Feed).filter(Feed.email_id == email_id).first()


def create_feed(email: str):
    web_domain = settings.site_url
    url = web_domain + "/rss/" + email
    email_id = email+"@"+settings.email_domain
    feed_dict = {"url":url, "domain":web_domain,
                    "email_id":email_id, "email": email}
    feed = Feed(**feed_dict)
    db.add(feed)
    db.commit()
    db.refresh(feed)
    logger.info(f'New feed created for {feed.email_id}')
    return feed


def get_feed_items(id:int, limit: int = 10):
    return db.query(FeedItem).filter(FeedItem.feed_id == id).order_by(FeedItem.id.desc()).limit(limit)


def create_feed_item(new_feed):
    db = SessionLocal()
    db_item = FeedItem(**new_feed)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item