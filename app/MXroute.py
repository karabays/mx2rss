import requests
from requests.auth import HTTPBasicAuth
import json
from urllib.parse import parse_qs

from app.log import logger

class MXroute:
    def __init__(self, userid, password, server):
        self.userid = userid
        self.password = password
        self.server = server


    def make_call(self, function, payload=None):
        auth=HTTPBasicAuth(self.userid, self.password)
        response = requests.get('https://' + self.server + '/' + function, auth=auth, params=payload)
        self.last_status_code = response.status_code
        self.last_response = response
        if response.status_code != 200:
            return None
        return parse_qs(response.text)


    def list_mail_domains(self):
        r = self.make_call('CMD_API_SHOW_DOMAINS')
        if r is None:
            return None
        return r


    def add_forwarder(self, email, domain, target):
        payload = {"action":"create", "domain":domain, "user":email, "email":target}
        r = self.make_call('CMD_API_EMAIL_FORWARDERS', payload=payload)
        if r['error']==['0']:
            logger.info(f"forwarder created: {email}@{domain} -> {target}")
            return {"result":"Success", "detail":f"forwarder created: {email}@{domain} -> {target}"}
        else:
            logger.warning(f"Forwarder creatin failed: {r['details']}")
            return {"result": "Fail", "detail":r['details']}
        return r


    def list_forwarders(self, email_domain):
        r = self.make_call('CMD_API_EMAIL_FORWARDERS', payload = {'domain':email_domain})
        if r is None:
            return None
        return r


    def delete_forwarder(self, email_from, email_to):
        pass


def test():
    import config
    settings = config.settings

    test_mx = MXroute(settings.dapanel_user, settings.dapanel_pass, settings.dapanel_url)
    print(test_mx.add_forwarder("test4", 'karabay.biz','mx2rss@karabay.biz'))
    print(test_mx.list_forwarders('karabay.biz'))
