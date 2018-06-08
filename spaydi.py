__author__ = "OguzBey"
__version__ = "1.0"
__email__ = "info@oguzbeg.com"

from modules import spider
import sys

B_RED = spider.B_RED
B_WHITE = spider.B_WHITE
B_BLUE = spider.B_BLUE
RESET = spider.RESET
YELLOW = spider.YELLOW
GREEN = spider.GREEN


class Main(object):
	def __init__(self, args):
		self.my_args = ["--url", "--cookie", "--level"]
		self.args = args

	def get_args(self, args):
		_args = dict()
		for i in range(0, len(args), 2):
			_args.update({args[i]:args[i+1]})
		return _args

	def check_args(self, args):
		for i in args:
			if i not in self.my_args:
				return False
		return True

	def start(self):
		_args = self.get_args(self.args)
		if not self.check_args(_args):
			help()
		if not '--url' in _args:
			help()
		_url = _args['--url']
		_level = _args['--level'] if '--level' in _args else None
		_cookie = _args['--cookie'] if '--cookie' in _args else None
		logo()
		try:
			spider.Spider(url=_url, level=_level, cookie=_cookie).go()
		except KeyboardInterrupt:
			print("Bye")
		except Exception as e:
			print(e)

def logo():
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
			{6}Github:{4} {7}{9}{4}
""".format(__version__, "0x150", __author__, B_WHITE, RESET, B_RED, YELLOW,
 		   GREEN, "http://python4hackers.com", "https://github.com/OguzBey/Spaydi")
	print(_1)


def help():
	logo()
	_text = """
			{0}--url{1} {2}<target_url>{1}
			{0}--level{1} {2}[1-5]{1} --> default 3 (Depth)
			{0}--cookie{1} {2}<cookie>{1} --> "key=value; key=value;"

	        {3}example:{1}
			{2}python3 spaydi.py --url {4}https://h4cktimes.com{1} --level {4}2{1}
	""".format(B_WHITE, RESET, GREEN, YELLOW, B_BLUE)
	print(_text)
	sys.exit(1)

def main():
	del sys.argv[0]
	argc = len(sys.argv)
	if argc in [2, 4, 6]:
		Main(sys.argv).start()
	else:
		help()

if __name__ == '__main__':
	main()
