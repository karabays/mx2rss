import uvicorn
from sqlalchemy.orm import Session

from fastapi import FastAPI, Request, Form, Depends, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi_utils.tasks import repeat_every
from fastapi_rss import RSSFeed, RSSResponse, Item, Category, CategoryAttrs, GUID

import uuid

import database as database
import models as models
import config as config
import MXroute as MXroute
from log import logger
import mail2feed as mail2feed

database.Base.metadata.create_all(bind=database.engine)

app = FastAPI()
templates = Jinja2Templates(directory="templates")
settings = config.settings
mx = MXroute.MXroute(settings.dapanel_user, settings.dapanel_pass, settings.dapanel_url)


def create_new_feed(email):
    if database.get_feed_by_email(email=email):
        raise HTTPException(status_code=400, detail="Email already registered")
    mx.add_forwarder(email, settings.email_domain, settings.inbox)
    feed = database.create_feed(email=email)
    first_feed(feed)

    return feed


def first_feed(feed):
    new_feed = mail2feed.first_item_dict
    new_feed['author'] = feed.email_id
    new_feed['feed_id'] = feed.id
    new_feed['guid'] = str(uuid.uuid4())
    database.create_feed_item(new_feed)

@app.on_event('startup')
@repeat_every(seconds=int(settings.fetch_frequency), logger=logger)
def check_mail():
    feeds = mail2feed.fetch_mails()
    for feed in feeds:
        feed['feed_id'] = database.get_feed_by_email_id(feed['to']).id
        del feed['to']
        database.create_feed_item(feed)


def serve_feeds(email):
    feed = database.get_feed_by_email(email)
    feed_items = database.get_feed_items(feed.id)

    items = []
    for item in feed_items:
        item_dict = vars(item)
        item_dict['guid'] = GUID(content=item.guid)
        items.append(item_dict)
    
    feed_data = {
        'title': "mx2RSS inbox - " + feed.email,
        'link': feed.url,
        'description': "mx2rss, free your inbox.",
        'last_build_date': feed.last_build_date,
        'item': items,
    }

    return feed_data


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
    feed_data = serve_feeds(email)
    feed = RSSFeed(**feed_data)
    return RSSResponse(feed)

if __name__ == "__main__":
    logger.info('*******************')
    logger.info("mx2rss is starting.")
    logger.info('*******************')
    uvicorn.run('main:app', host='0.0.0.0', log_level='info', reload=True)
    logger.info('******************')
    logger.info("mx2rss is closing.")
    logger.info('******************')