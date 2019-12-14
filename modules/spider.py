from . import browser
from . import crawler
import re
from colorama import Fore, Style
import queue
from threading import Thread
import logging


B_BLUE = Style.BRIGHT+Fore.BLUE
B_WHITE = Style.BRIGHT+Fore.WHITE
B_RED = Style.BRIGHT+Fore.RED
B_CYAN = Style.BRIGHT+Fore.CYAN
RESET = Style.RESET_ALL
GREEN = Fore.GREEN
YELLOW = Fore.YELLOW


class Spider(object):

    def __init__(self, url, level=None, cookie=None, fast=None):
        self.logger = logging.getLogger("Spider")
        self.logger.setLevel(logging.DEBUG)
        handler = logging.FileHandler("Spaydi.log")
        handler.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
        self.level = level if level is not None and level in [1,2,3,4,5] else 3
        self.fast_mode = fast if fast is not None else False
        self.cookie = cookie
        self.target_url = url
        self.visited_urns = []
        self.visited_urls = []
        self.output_forms = []
        self.visit_urls = []
        self.printed_action = []
        self.target_domain = self.get_domain(self.target_url)
        self.browser = browser.Browser()
        self.crawler = crawler.Crawler()

    def get_domain(self, url):
        _domain = re.findall(r'https?://(.*?)\/', url)
        _domain2 = re.findall(r'https?://(.*?)$', url)
        r_domain =  _domain[0] if _domain else _domain2[0]
        return r_domain

    def set_link(self, link):
        if "javascript:" in link:
            return False
        if link.startswith("http://") or link.startswith("https://"):
            _domain = self.get_domain(link)
            if _domain == self.target_domain:
                return link
            else:
                return False
        else:
            link = "http://{}/{}".format(self.target_domain, link)
            return link

    def print_forms(self, forms):
        _form = ""
        print("{1}Page Title:{2} {3}{0}{2}".format(self.browser.page_title,
                                                   B_BLUE, RESET, GREEN))
        print("{1}Set-Cookie:{2} {3}{0}{2}".format(self.browser.set_cookie,
                                                   B_BLUE, RESET, GREEN))
        for i in forms:
            if i['form_action'] in self.printed_action:
                continue
            print("-"*30+"<FORM>"+"-"*30)
            print("{1}Page URL :{2} {3}{0}{2}".format(i['url'], B_BLUE, RESET,
                                                      GREEN))
            print("{1}ACTION:{2} {3}{0}{2}".format(i['form_action'].lower(),
                                                   B_BLUE, RESET, GREEN))
            print("{1}METHOD:{2} {3}{0}{2}".format(i['form_method'].upper(),
                                                   B_BLUE, RESET, GREEN))
            _form += "Page Title: {}\n".format(self.browser.page_title)
            _form += "Set-Cookie: {}\n".format(self.browser.set_cookie)
            _form += "Page Url: {}\n".format(i['url'])
            _form += "ACTION: {}\n".format(i['form_action'].lower())
            _form += "METHOD: {}\n".format(i['form_method'].upper())
            for input in i['inputs']:
                _form += "[input] "
                _text = "{0}[input]{1}{2} ".format(B_BLUE, RESET, GREEN)
                _name = input['name']
                _type = input['type']
                _value = input['value']
                _placeholder = input['placeholder']
                _text += "{1}name{2}={3}'{0}'{2}, ".format(_name, YELLOW, RESET,
                                                            GREEN) if _name \
                                                            != "" else ""
                _form += "name='{}', ".format(_name) if _name != "" else ""
                _text += "{1}type{2}={3}'{0}'{2}, ".format(_type, YELLOW, RESET,
                                                            GREEN) if _type \
                                                            != "" else ""
                _form += "type='{}', ".format(_type) if _type != "" else ""
                _text += "{1}value{2}={3}'{0}{2}', ".format(_value, YELLOW,
                                                            RESET, GREEN) \
                                                            if _value != "" \
                                                            else ""
                _form += "value='{}', ".format(_value) if _value != "" else ""
                _text += "{1}placeholder{2}={3}'{0}'{2}".format(_placeholder,
                                                                YELLOW, RESET,
                                                                GREEN) \
                                                                if _placeholder \
                                                                != "" else ""
                _form += "placeholder='{}', ".format(_placeholder) if _placeholder \
                                                     != "" else ""
                _form += "\n"
                print(_text+RESET)
            self.printed_action.append(i['form_action'])
            self.output_forms.append(_form)
            print("-"*30+"</FORM>"+"-"*30)

    def clean_link(self, link):
        point = False
        _link = ""
        if "#" in link:
            for i in link:
                if i == "#" or point is True:
                    point = True
                    continue
                _link += i
            return _link
        return link

    def just_urn(self, link):
        if link.startswith("https://"):
            link = link[8::]
            return link
        link = link[7::]
        return link

    def loop(self):
        # self.logger.info("loop() started.")
        _url_list = []
        for link in self.visit_urls:
            link = self.clean_link(link)
            if self.just_urn(link) in self.visited_urns:
                continue
            stat = self.browser.get(url=link, cookie=self.cookie)
            print("{1}{0}{2}".format("--"*40, B_RED, RESET))
            print("{1}[GET]{2} {0}".format(link, B_CYAN, RESET))
            self.visited_urns.append(self.just_urn(link))
            self.visited_urls.append(link)
            if stat in [200, 302, 301]:
                forms = self.crawler.get_forms(self.browser.page_source, link)
                self.print_forms(forms)
                links = self.crawler.get_urls(self.browser.page_source)
                for i in links:
                    _link = self.set_link(i)
                    if _link and self.just_urn(_link) not in self.visited_urns:
                        _url_list.append(_link)
        del self.visit_urls[:]
        _url_list = list(set(_url_list))
        self.visit_urls = _url_list[:]
        del _url_list

    def t_process(self, link):
        # self.logger.info("t_process() started.")
        _url_list = []
        stat = self.browser.get(url=link, cookie=self.cookie)
        print("{1}{0}{2}".format("--"*40, B_RED, RESET))
        print("{1}[GET]{2} {0} {3}".format(link, B_CYAN, RESET, stat))
        self.visited_urns.append(self.just_urn(link))
        self.visited_urls.append(link)
        if stat in [200, 302, 301]:
            forms = self.crawler.get_forms(self.browser.page_source, link)
            self.print_forms(forms)
            links = self.crawler.get_urls(self.browser.page_source)
            for i in links:
                _link = self.set_link(i)
                if _link and self.just_urn(_link) not in self.visited_urns:
                    _url_list.append(_link)
        return _url_list

    def t_loop(self):
        # self.logger.info("t_loop() started.")
        _url_list = []
        que = queue.Queue()
        thread_list = []
        th_count = 0
        max_thrad = 5
        l_visit_urls = len(self.visit_urls)
        for link in self.visit_urls:
            link = self.clean_link(link)
            if self.just_urn(link) in self.visited_urns:
                l_visit_urls -= 1
                continue
            t = Thread(target=lambda q, arg1: q.put(self.t_process(arg1)), \
                       args=(que, link))
            t.start()
            thread_list.append(t)
            th_count += 1
            l_visit_urls -= 1
            self.logger.info("Started Thread-{}".format(th_count))
            if th_count%max_thrad == 0:
                self.logger.info("Waiting for Thread Process...")
                for t in thread_list:
                    t.join()
                self.logger.info("Thread Process Finished..")
            elif l_visit_urls < 5:
                self.logger.info("Waiting for Thread Process...")
                for t in thread_list:
                    t.join()
                self.logger.info("Thread Process Finished..")
        while not que.empty():
            _url_list.extend(que.get())
        del self.visit_urls[:]
        _url_list = list(set(_url_list))
        self.visit_urls = _url_list[:]
        del _url_list

    def go(self):
        self.logger.info("go() started.")
        # level 1
        stat = self.browser.get(self.target_url, cookie=self.cookie)
        print("{1}{0}{2}".format("--"*40, B_RED, RESET))
        if stat in [200, 302, 301]:
            forms = self.crawler.get_forms(self.browser.page_source, self.target_url)
            self.print_forms(forms)
            links = self.crawler.get_urls(self.browser.page_source)
            for i in links:
                _link = self.set_link(i)
                if _link:
                    self.visit_urls.append(_link)
            self.visit_urls = list(set(self.visit_urls))
            self.logger.info("t_loop() started with Fast mode")
            if self.fast_mode:
                for i in range(self.level-1):
                    self.logger.info("t_loop() started with Fast mode")
                    self.t_loop()
            else:
                for i in range(self.level-1):
                    self.logger.info("t_loop() started with Normal mode")
                    self.loop()
        else:
            print(stat)
        return self.visited_urls, self.output_forms

if __name__ == '__main__':
    pass
