import models
import config
import datetime as dt

settings = config.settings

first_item_dict = {'title': 'Hello There',
                'description' : 'This is the first entry. Whenever a new mail arrives to email address you created, it will be published here. Hopefully this will reduce the number of emails in your inbox.<br>Have fun!',
                'pub_date': dt.datetime.today()}

