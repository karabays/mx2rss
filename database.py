import datetime

from sqlalchemy import create_engine, Boolean, Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship, Session

from fastapi_rss import RSSFeed, RSSResponse, Item, Category, CategoryAttrs, GUID

import models
from config import config

SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

domain = config.domain

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
    feed_id = Column(Integer, ForeignKey("feeds.id"))
    feed = relationship("Feed", back_populates="items")


def get_feed_by_email(email: str):
    db = SessionLocal()
    return db.query(Feed).filter(Feed.email == email).first()


def create_feed(email: str):
    db = SessionLocal()
    url = domain["site"] + "/rss/" + email
    email_id = email+"@"+domain['email']
    web_domain = domain['site']
    feed_dict = {"url":url, "domain":web_domain,
                    "email_id":email_id, "email": email}
    feed = Feed(**feed_dict)
    db.add(feed)
    db.commit()
    db.refresh(feed)
    return feed


def get_items(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Item).offset(skip).limit(limit).all()


# def create_feed_item(db: Session, item: models.ItemCreate, user_id: int):
#     db_item = models.Item(**item.dict(), owner_id=user_id)
#     db.add(db_item)
#     db.commit()
#     db.refresh(db_item)
#     return db_item


test = {
        'title': 'Test 2',
        'link': '',
        'description': "",
        'language': 'en-us',
        'copyright': 'Copyright',
        'last_build_date': datetime.datetime(
            year=2021, month=1, day=11,
            hour=2, minute=49, second=32
        ),
        'managing_editor': 'self@example.com',
        'webmaster': 'self@example.com',
        'generator': 'Test',
        'ttl': 30,
        'item': [
            Item(
                title='Test',
                link='https://www.example.com/projects/2020/12/31/test',
                description='',
                author='Dogeek',
                category=Category(
                    content='0001',
                    attrs=CategoryAttrs(domain='test')
                ),
                pub_date=datetime.datetime(
                    year=2020, month=12, day=31,
                    hour=12, minute=40, second=16,
                ),
                guid=GUID(content='abcdefghijklmnopqrstuvwxyz')
            )
        ],
    }

feed_data = {"test":test}
