__author__ = "OguzBey"
__version__ = "1.5.1"
__email__ = "info@oguzbeg.com"

from modules import spider
from modules import crawler
from modules import sqli
import sys
import os
import logging


B_RED = spider.B_RED
B_WHITE = spider.B_WHITE
B_BLUE = spider.B_BLUE
RESET = spider.RESET
YELLOW = spider.YELLOW
GREEN = spider.GREEN

logger = logging.getLogger("spaydi")
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler("Spaydi.log")
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.info("Started the program.")


class Main(object):
    def __init__(self, args):
        self.crawler = crawler.Crawler()
        self.sqli = sqli.SqlInjection()
        self.logger = logging.getLogger("Spaydi-Main")
        self.logger.setLevel(logging.DEBUG)
        self.logger.addHandler(handler)
        self.injectable = []
        self.my_args = ["--url", "--cookie", "--level", "--fast", "--check"]
        self.check_list = ["sqli"]
        self.args = args
        self.current_path = os.path.dirname(os.path.realpath(__file__))
        self.links_file = "links.txt"
        self.forms_file = "forms.txt"
        self.outputs_dir = "outputs"
        self.links_file_path = os.path.join(self.current_path, self.outputs_dir\
                                            , self.links_file)
        self.forms_file_path = os.path.join(self.current_path, self.outputs_dir\
                                            , self.forms_file)
        if not os.path.exists(os.path.join(self.current_path, self.outputs_dir)):
            os.mkdir(os.path.join(self.current_path, self.outputs_dir))
            self.logger.info("Created outputs(DIR)")

    def get_args(self, args):
        self.logger.info("get_args() started.")
        _args = dict()
        for i in range(0, len(args), 2):
            _args.update({args[i]:args[i+1]})
		# self.logger.debug("get_args() return --> {}".format(_args))
        return _args

    def check_args(self, args):
        self.logger.info("check_args() started.")
        for i in args:
            if i not in self.my_args:
                return False
        return True

    def write_file(self, listt, path, tire=False):
        self.logger.info("write_file() started.")
        if tire is False:
            with open(path, "w") as fl:
                _write = ""
                for i in listt:
                    _write += "{}\n".format(i)
                _write = _write.rstrip("\n")
                fl.write(_write)
        else:
            with open(path, "w") as fl:
                _write = ""
                for i in listt:
                    _write += "--"*30+"\n"
                    _write += "{}\n".format(i)
                    _write += "--"*30+"\n"
                _write = _write.rstrip("\n")
                fl.write(_write)

    def start(self):
        self.logger.info("start() started.")
        _fast = False
        if "--fast" not in self.args and len(self.args) in [3,5,7,9]:
            help()
        elif "--fast" in self.args and len(self.args) in [3,5,7,9]:
            _fast = True
            self.args.remove('--fast')
        _args = self.get_args(self.args)
        if not self.check_args(_args):
            help()
        if not '--url' in _args:
            help()
        _check = _args['--check'] if '--check' in _args else None
        if _check: # sqli, XSS, ...
            _check = _check.split(",")
            for i in _check:
                if i not in self.check_list:
                    help()
        _url = _args['--url']
        _level = _args['--level'] if '--level' in _args else None
        _cookie = _args['--cookie'] if '--cookie' in _args else None
        logo()
        self.spaydi = spider.Spider(url=_url, level=_level, cookie=_cookie, fast=_fast)
        try:
            urls, forms = self.spaydi.go()
            self.exit_o = "[+] Done."
        except KeyboardInterrupt:
            urls = self.spaydi.visited_urls
            forms = self.spaydi.output_forms
            self.exit_o = "[-] Exit."
        except:
            urls = self.spaydi.visited_urls
            forms = self.spaydi.output_forms
            self.exit_o = "[-] Exit."
            _, err, _ = sys.exc_info()
            self.logger.error("start() --> {}".format(err))
            self.logger.info("Exit.")
        self.write_file(urls, self.links_file_path)
        self.write_file(forms, self.forms_file_path, tire=True)
        print(B_RED+"--"*30+RESET)
        print("[+]{0} Detected url parameters :{1}".format(B_BLUE, RESET))
        for url in urls:
            _text = ""
            uparameters = self.crawler.get_uparameters(url=url)
            if uparameters:
                for param in uparameters:
                    _url = {}
                    _url.update({'url':url, 'param':param})
                    self.injectable.append(_url)
                print("{0}[URL] >> {1}{3}{2}{1}".format(B_BLUE, RESET, url, GREEN))
                for i in uparameters:
                    _text += "{0}{2}{1}, ".format(YELLOW, RESET, i)
                _text = _text[:-2]
                print("{0}[P] >> {1}{2}".format(B_BLUE, RESET, _text))
        print(B_RED+"--"*30+RESET)
        ### CHECK VULN ####
        if _check and "sqli" in _check:
            ### SQLi ####
            _check.remove('sqli')
            print("{2}[+]{1} {0}Starting Sqli...{1}".format(B_BLUE, RESET, B_WHITE))
            self.sqli.start(urls=self.injectable)
            print(B_RED+"--"*30+RESET)
            ###### END #####
        print("[+]  {} : {}".format("Links", self.links_file_path))
        print("[+]  {} : {}".format("Forms", self.forms_file_path))
        print("[+]  {}:  {}".format("Logs:", os.path.join(self.current_path, "Spaydi.log")))
        print(self.exit_o)
        self.logger.info("Exit.")

def logo():
    logger.info("logo() started.")
    _1 = """

{3}		  ██████  ██▓███   ▄▄▄     ▓██   ██▓▓█████▄  ██▓
		▒██    ▒ ▓██░  ██▒▒████▄    ▒██  ██▒▒██▀ ██▌▓██▒
		░ ▓██▄   ▓██░ ██▓▒▒██  ▀█▄   ▒██ ██░░██   █▌▒██▒
		  ▒   ██▒▒██▄█▓▒ ▒░██▄▄▄▄██  ░ ▐██▓░░▓█▄   ▌░██░{4}{5}
		▒██████▒▒▒██▒ ░  ░ ▓█   ▓██▒ ░ ██▒▓░░▒████▓ ░██░
		▒ ▒▓▒ ▒ ░▒▓▒░ ░  ░ ▒▒   ▓▒█░  ██▒▒▒  ▒▒▓  ▒ ░▓
		░ ░▒  ░ ░░▒ ░       ▒   ▒▒ ░▓██ ░▒░  ░ ▒  ▒  ▒ ░
		░  ░  ░  ░░         ░   ▒   ▒ ▒ ░░   ░ ░  ░  ▒ ░
		      ░                 ░  ░░ ░        ░     ░
		                            ░ ░      ░
{4}
                        {6}By{4} {7}{1}{4}, {7}{2}{4}
                        {6}Version:{4} {7}{0}{4}
                        {6}Site:{4} {7}{8}{4}
""".format(__version__, "0x150", __author__, B_WHITE, RESET, B_RED, YELLOW,
           GREEN, "http://python4hackers.com")
    print(_1)


def help():
    logger.info("help() started.")
    logo()
    _text = """
            {0}--url{1} {2}<target_url>{1}
            {0}--level{1} {2}[1-5]{1} --> default 3 (Depth)
            {0}--cookie{1} {2}<cookie>{1} --> "key=value; key=value;"
            {0}--fast{1} --> Fast Scan ! (5 Threads)
            {0}--check{1} {2}[sqli]{1} --> check sqli vuln

        {3}Examples:{1}
            {2}python3 spaydi.py{1} --url {4}https://h4cktimes.com{1} --level {4}2{1}
            {2}python3 spaydi.py{1} --url {4}http://python4hackers.com{1} --check {4}sqli{1}
    """.format(B_WHITE, RESET, GREEN, YELLOW, B_BLUE)
    print(_text)
    logger.info("Exit.")
    sys.exit(1)

def main():
    logger.info("main() started.")
    del sys.argv[0]
    argc = len(sys.argv)
    if argc in [2, 3, 4, 5, 6, 7, 9]:
        Main(sys.argv).start()
    else:
        help()

if __name__ == '__main__':
    main()
