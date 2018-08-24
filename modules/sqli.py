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
        self.tested_uparams_syntax = []
        self.tested_uparams_numeric = []
        self.r_html = re.compile('<.*?>')
        # self.current_params = []
        # self.current_param = ""
        # self.current_url = ""
        self.errs = ["MySQL server version for the right syntax to use near",
                     "Unclosed quotation mark after the character string",
                     "quoted string not properly terminated",
                     "You have an error in your SQL syntax"]

    def is_numeric(self, val):
        for i in val:
            _chrcode = ord(i)
            if _chrcode < 48 or _chrcode > 57:
                # not numeric
                return False
        return True


    def numeric(self, url):
        # numerical test
        # id=1+1 --> id = 2 ?
        _keyVal = url['param'].split("=")
        _key = _keyVal[0] # key
        _val = _keyVal[1] # value
        _url = url['url'] # url
        _tested = "{}--{}".format(_url.split('?')[0], _key)
        if _tested in self.tested_uparams_numeric:
            return 3 # continue, if we tested this -> url+parameter
        if not self.is_numeric(_val):
            return 0 # False
        if self.br.get(_url) != 200:
            return 4 # bad page
        self.tested_uparams_numeric.append(_tested)
        my_id = int(_val)
        new_id = my_id + 1
        _param = "{}={}".format(_key, new_id) # new param
        _url = _url.replace(url['param'], _param)
        url['param'] = _param
        while self.br.get(_url) != 200:
            new_id += 1
            _param = "{}={}".format(_key, new_id) # new param
            _url = _url.replace(url['param'], _param)
            url['param'] = _param
        # okay we found new id
        # step 1
        _fsource = re.sub(self.r_html, '', self.br.page_source)
        _ftitle = self.br.page_title
        # step 2
        _addThis = new_id - my_id
        _param = "{0}={1}+{2}".format(_key, my_id, _addThis)
        _url = _url.replace(url['param'], _param)
        if self.br.get(_url) != 200:
            return 0 # False
        _lsource = re.sub(self.r_html, '', self.br.page_source)
        _ltitle = self.br.page_title
        # final
        if _lsource == _fsource:
            if _ltitle and _ftitle and _ltitle == _ftitle:
                # oh yes sqli
                return 1 # True
            return 2 # maybe
        return 0

    def syntax_err(self, url):
        # test syntax error
        _keyVal = url['param'].split("=")
        _key = _keyVal[0] # key
        _val = "{}'a".format(_keyVal[1]) # value'a
        _url = url['url'] # url
        _param = "{}={}".format(_key, _val) # new param
        _tested = "{}--{}".format(_url.split('?')[0], _key)
        # step 1
        if _tested in self.tested_uparams_syntax:
            return 3 # continue, if we tested this -> url+parameter
        stat = self.br.get(_url)
        _old_text = re.sub(self.r_html, '', self.br.page_source)
        # step 2
        _url = _url.replace(url['param'], _param)
        stat = self.br.get(_url)
        _new_text = re.sub(self.r_html, '', self.br.page_source)
        self.tested_uparams_syntax.append(_tested)
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
        # urls --> [ {'url':val, 'param':val}, ... ]
        # param --> key=val
        # url --> full url
        for url in urls:
            # syntax test
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
            # numeric test
            vuln = self.numeric(url)
            if vuln == 1:
                _text = "{0}[+]{1} {2}Numeric Error Found :{1}"
                _text = _text.format(B_WHITE, RESET, B_RED)
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
    #    i = ast.literal_eval(i)
    #    b.append(i)
    # sqli = SqlInjection()
    # sqli.start(urls=b)
