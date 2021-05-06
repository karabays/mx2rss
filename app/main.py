import uvicorn
from sqlalchemy.orm import Session

from fastapi import FastAPI, Request, Form, Depends, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi_utils.tasks import repeat_every
from fastapi_rss import RSSFeed, RSSResponse, Item, Category, CategoryAttrs, GUID

import uuid

import app.database as database
import app.models as models
import app.config as config
import app.MXroute as MXroute
from app.log import logger
import app.mail2feed as mail2feed

database.Base.metadata.create_all(bind=database.engine)

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="./templates")
settings = config.settings
mx = MXroute.MXroute(settings.dapanel_user, settings.dapanel_pass, settings.dapanel_url)


def create_new_feed(feed: models.FeedBase):
    if database.get_feed_by_email(email=feed.email):
        return {"result":'Fail', 'detail':"Email already registered"}
    mx_result = mx.add_forwarder(feed.email, settings.email_domain, settings.inbox)
    if mx_result['result'] == "Success": 
        new_feed = vars(database.create_feed(email=feed.email))
        new_feed['result'] = 'Success'
        first_feed(new_feed)
        return new_feed
    else:
        return mx_result


def first_feed(feed):
    new_feed = mail2feed.first_item_dict
    new_feed['author'] = feed['email_id']
    new_feed['feed_id'] = feed['id']
    new_feed['guid'] = str(uuid.uuid4())
    database.create_feed_item(new_feed)


@app.on_event('startup')
@repeat_every(seconds=int(settings.fetch_frequency), logger=logger)
def check_mail():
    mails = mail2feed.fetch_mails()
    if mails:
        for mail in mails:
            feed = database.get_feed_by_email_id(mail['to'])
            if feed:
                mail['feed_id'] = feed.id
                del mail['to']
                database.create_feed_item(mail)


def serve_feeds(email):
    feed = database.get_feed_by_email(email)
    if feed is None:
        raise HTTPException(404, detail='Feed do not exist.')
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
    return create_new_feed(feed)


@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "domain": settings.email_domain})


@app.post("/new/", response_class=HTMLResponse)
def new_routing(request: Request, email: str = Form(...)):
    new_feed = models.FeedBase(email=email)
    result = create_new_feed(new_feed)
    result['request'] = request
    print(result)
    if result['result'] == 'Fail':
        return templates.TemplateResponse("fail.html", result)
    else:
        return templates.TemplateResponse("success.html", result)


@app.get('/rss/{email}')
def serve_rss(email):
    feed_data = serve_feeds(email)
    feed = RSSFeed(**feed_data)
    return RSSResponse(feed)

if __name__ == "__main__":
    logger.info('*******************')
    logger.info("mx2rss is starting.")
    logger.info('*******************')
    uvicorn.run('main:app', host='0.0.0.0', port=9123, log_level='info', reload=True)
    logger.info('******************')
    logger.info("mx2rss is closing.")
    logger.info('******************')