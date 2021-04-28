from pydantic import BaseModel

class FeedBase(BaseModel):
    email: str

class Feed(FeedBase):
    id: int
    email_id: str
    domain: str
    url: str

    class Config:
        orm_mode = True