import uvicorn
from fastapi import FastAPI, Request, Form, Depends, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi_rss import RSSFeed, RSSResponse
from sqlalchemy.orm import Session

import database
import models
import config
import MXroute

database.Base.metadata.create_all(bind=database.engine)

app = FastAPI()
templates = Jinja2Templates(directory="templates")
settings = config.settings
mx = MXroute.MXroute(settings.dapanel_user, settings.dapanel_pass, settings.dapanel_url)


def create_new_feed(email):
    if database.get_feed_by_email(email=email):
        raise HTTPException(status_code=400, detail="Email already registered")
    return database.create_feed(email=email)


@app.post("/api/new/", response_model=models.Feed)
def new_routing_api(feed: models.FeedBase):
    return create_new_feed(email=feed.email)

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "domain": settings.email_domain})

@app.post("/new/", response_class=HTMLResponse)
def new_routing(request: Request, email: str = Form(...)):
    new_dict = vars(create_new_feed(email))
    new_dict['request'] = request
    return templates.TemplateResponse("new.html", new_dict)

@app.get('/rss/{email}')
def serve_rss(email):
    email = "test"
    feed_data = database.feed_data[email]
    feed = RSSFeed(**feed_data)
    return RSSResponse(feed)

if __name__ == "__main__":
    uvicorn.run('main:app', host='127.0.0.1', port=8080, log_level='info', reload=True)