import urllib.request
from urllib.error import HTTPError
from urllib.parse import urlencode, quote
from random import choice, randint
import os
import ssl
import logging
import sys


class Browser(object):

    def __init__(self):
        self.logger = logging.getLogger("Browser")
        self.logger.setLevel(logging.DEBUG)
        handler = logging.FileHandler("Spaydi.log")
        handler.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
        self.page_source = None
        self.page_title = None
        self.current_url = None
        self.set_cookie = None
        self.gcontext = ssl.SSLContext(ssl.PROTOCOL_TLSv1)
        self.user_agents_file = "user-agents.txt"
        self.current_path = os.path.dirname(os.path.realpath(__file__))
        self.fullpath_useragent = os.path.join(self.current_path, self.user_agents_file)
        with open(self.fullpath_useragent, "r") as fl:
            self.useragents = fl.read().splitlines()

    def _header(self, cookie=None):
        header = {'User-Agent':choice(self.useragents)}
        header.update({'Referer':'https://www.gogle.com'})
        fw_ip = "{}.{}.{}.{}".format(randint(1,255), randint(1,255),
                                     randint(1,255), randint(1,255))
        header.update({'X-Forwarded-Host': '{}'.format(fw_ip)})
        if cookie is None:
            return header
        header.update({'Cookie':cookie})
        return header

    def _set_info(self, resp):
        # self.logger.info("_set_info() started.")
        self.page_source = str(resp.read(), 'utf-8', errors='ignore')
        self.current_url = resp.url
        try:
            self.page_title = self.page_source.split('<title>')[1].split('</title>')[0]
        except:
            _, err, _ = sys.exc_info()
            self.logger.error("_set_info() --> {}".format(err))
            self.page_title = None
        _cookie = resp.getheader('set-cookie')
        self.set_cookie = _cookie if _cookie is not None else "No-Cookie"

    def get(self, url:str, cookie=None) -> int:
        try:
            _req = urllib.request.Request(url=url, headers=self._header(cookie))
            _resp = urllib.request.urlopen(_req)
            self._set_info(_resp)
            self.logger.info("get() [GET] --> {} {}".format(url, _resp.status))
            return _resp.status
        except HTTPError as e:
            _, err, _ = sys.exc_info()
            self.logger.error("get() -->{2} {0} {1}".format(err, url, e.code))
            return e.code
        except:
            _, err, _ = sys.exc_info()
            self.logger.error("get() --> {}".format(err))
            _req = urllib.request.Request(url=url, headers=self._header(cookie))
            _resp = urllib.request.urlopen(_req, context=self.gcontext)
            self._set_info(_resp)
            return _resp.status


    def post(self, url:str, data:dict) -> int:
        try:
            data = urlencode(data)
            _req = urllib.request.Request(url=url, data=data,
                                          headers=self._header())
            _resp = urllib.request.urlopen(_req, context=self.gcontext)
            self_set_info(_resp)
            self.logger.info("post() [POST] --> {} {}".format(url, _resp.status))
            return _resp.status
        except HTTPError as e:
            _, err, _ = sys.exc_info()
            self.logger.error("post() --> {}".format(err))
            return e.code
