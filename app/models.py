from pydantic import BaseModel
from datetime import date, datetime, time, timedelta

class FeedBase(BaseModel):
    email: str

class Feed(FeedBase):
    id: int
    email_id: str
    domain: str
    url: str

    class Config:
        orm_mode = True



class FeedItemBase(BaseModel):
    pass

class FeedItem(FeedItemBase):
    guid: str
    title: str
    description: str
    author: str
    pub_date: datetime

    class Config:
        orm_mode = True