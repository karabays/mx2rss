import datetime as dt
from log import logger
from imap_tools import MailBox, AND

import models as models
import config as config

settings = config.settings

first_item_dict = {'title': 'Hello There',
                'description' : 'This is the first entry. Whenever a new mail arrives to email address you created, it will be published here. Hopefully this will reduce the number of emails in your inbox.<br>Have fun!',
                'pub_date': dt.datetime.today()}


def fetch_mails():
    mailbox = MailBox(settings.inbox_url)
    mailbox.login(settings.inbox, settings.inbox_pass)
    msgs = mailbox.fetch(AND(seen=False))
    feeds = []
    for msg in msgs:
        feed = {'title':msg.subject, "description":msg.html, 
        'author': msg.from_, 'pub_date':msg.date,
        'guid':msg.uid, 'to': msg.to[0]}
        feeds.append(feed)
        logger.info(f"New message retrieved for {msg.to}")
    if len(feeds) == 0:
        logger.info("No new messages.")
    return feeds


