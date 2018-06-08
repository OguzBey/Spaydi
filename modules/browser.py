import urllib.request
from urllib.error import HTTPError
from urllib.parse import urlencode, quote
from random import choice, randint
import os
import ssl


class Browser(object):

	def __init__(self):
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
		self.page_source = str(resp.read(), 'utf-8', errors='ignore')
		self.current_url = resp.url
		try:
			self.page_title = self.page_source.split('<title>')[1].split('</title>')[0]
		except:
			self.page_title = None
		_cookie = resp.getheader('set-cookie')
		self.set_cookie = _cookie if _cookie is not None else "No-Cookie"

	def get(self, url:str, cookie=None) -> int:
		try:
			_req = urllib.request.Request(url=url, headers=self._header(cookie))
			_resp = urllib.request.urlopen(_req, context=self.gcontext)
			self._set_info(_resp)
			return _resp.status
		except HTTPError as e:
			return e.code

	def post(self, url:str, data:dict) -> int:
		try:
			data = urlencode(data)
			# url = quote(url, safe=':')
			_req = urllib.request.Request(url=url, data=data,
										  headers=self._header())
			_resp = urllib.request.urlopen(_req, context=self.gcontext)
			self_set_info(_resp)
			return _resp.status
		except HTTPError as e:
			return e.code
