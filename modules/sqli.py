# from . import browser
from . import browser
import re
from colorama import Fore, Style

B_BLUE = Style.BRIGHT+Fore.BLUE
B_WHITE = Style.BRIGHT+Fore.WHITE
B_RED = Style.BRIGHT+Fore.RED
RESET = Style.RESET_ALL
GREEN = Fore.GREEN
YELLOW = Fore.YELLOW


class SqlInjection(object):

	def __init__(self):
		self.br = browser.Browser()
		self.tested_uparams = []
		self.r_html = re.compile('<.*?>')
		self.errs = ["MySQL server version for the right syntax to use near",
			   "Unclosed quotation mark after the character string",
			   "quoted string not properly terminated",
			   "You have an error in your SQL syntax"]

	def numeric(self):
		# numerical test
		# id=1+1 --> id = 2 ?
		pass

	def syntax_err(self, url):
		# test syntax error
		_params = url['param'].split("=")
		_key = _params[0]
		_val = "{}'a".format(_params[1])
		_url = url['url']
		_param = "{}={}".format(_key, _val)
		_tested = "{}--{}".format(_url.split('?')[0], _key)
		# step 1
		if _tested in self.tested_uparams:
			return 3 # continue, We tested this -> url+parameter
		stat = self.br.get(_url)
		_old_text = re.sub(self.r_html, '', self.br.page_source)
		# step 2
		_url = _url.replace(url['param'], _param)
		stat = self.br.get(_url)
		_new_text = re.sub(self.r_html, '', self.br.page_source)
		self.tested_uparams.append(_tested)
		if _old_text == _new_text:
			return 0 # False
		for err in self.errs:
			if err in _new_text:
				return 1 # True
		return 2 # Possible


	def ratio(self):
		# first content vs second content
		pass

	def start(self, urls):
		# start process
		# like a main func.
		for url in urls:
			vuln = self.syntax_err(url)
			if vuln == 1:
				_text = "{0}[+]{1} {2}Syntax Error Found :{1}"
				_text = _text.format(B_WHITE, RESET, B_RED)
				print("{} {} --> {}".format(_text, url['url'], url['param']))
			elif vuln == 0:
				_text = "{0}[-]{1} {2}No Syntax Error :{1}"
				_text = _text.format(B_WHITE, RESET, GREEN)
				print("{} {} --> {}".format(_text, url['url'], url['param']))
			elif vuln == 2:
				_text = "{0}[?]{1} {2}Maybe Sqli :{1}"
				_text = _text.format(B_WHITE, RESET, YELLOW)
				print("{} {} --> {}".format(_text, url['url'], url['param']))


if __name__ == '__main__':
	pass
	# b = []
	# a = open('test.txt','r').read().splitlines()
	# import ast
	# for i in a:
	# 	i = ast.literal_eval(i)
	# 	b.append(i)
	# sqli = SqlInjection()
	# sqli.start(urls=b)
