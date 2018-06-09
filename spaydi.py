__author__ = "OguzBey"
__version__ = "1.1.0"
__email__ = "info@oguzbeg.com"

from modules import spider
import sys
import os

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

	def write_file(self, listt, path, tire=False):
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
		_args = self.get_args(self.args)
		if not self.check_args(_args):
			help()
		if not '--url' in _args:
			help()
		_url = _args['--url']
		_level = _args['--level'] if '--level' in _args else None
		_cookie = _args['--cookie'] if '--cookie' in _args else None
		logo()
		self.spaydi = spider.Spider(url=_url, level=_level, cookie=_cookie)
		try:
			urls, forms = self.spaydi.go()
			self.write_file(urls, self.links_file_path)
			self.write_file(forms, self.forms_file_path, tire=True)
			print("[+]  {} : {}".format("Links", self.links_file_path))
			print("[+]  {} : {}".format("Forms", self.forms_file_path))
			print("[-] Done.")
		except KeyboardInterrupt:
			if self.spaydi.output_forms and self.spaydi.visited_urls:
				self.write_file(self.spaydi.visited_urls, self.links_file_path)
				self.write_file(self.spaydi.output_forms, self.forms_file_path, tire=True)
				print("[+]  {} : {}".format("Links", self.links_file_path))
				print("[+]  {} : {}".format("Forms", self.forms_file_path))
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
""".format(__version__, "0x150", __author__, B_WHITE, RESET, B_RED, YELLOW,
 		   GREEN, "http://python4hackers.com")
	print(_1)


def help():
	logo()
	_text = """
			{0}--url{1} {2}<target_url>{1}
			{0}--level{1} {2}[1-5]{1} --> default 3 (Depth)
			{0}--cookie{1} {2}<cookie>{1} --> "key=value; key=value;"

	        {3}Example:{1}
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
