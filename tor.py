import urllib2
from batch import Batch, Timeout

class Tor(Batch):
	cmd_start = "sh ./test.sh"
	cmd_check = 'curl -s https://check.torproject.org/?lang=en_US'

	def __init__(self, log, output):		
		Batch.__init__ (self, self.cmd_start)
		self.set_new_writer (output)
		self.log = log
	'''
	def check(self, sec = 1):
		try:
			html = urllib2.urlopen('https://check.torproject.org/?lang=en_US', timeout = sec).read()
		except:
			self.log("Checking tor online status is taking too long!")
			return False
		else:
			return True if "Congratulations. This browser is" in html else False
	'''
	def check (self, callback, sec = 1):
		def parser (fd):
			callback ('Congratulations. This browser is' in fd.read())

		self.set_cmd (self.cmd_check, should_be_root = False)
		self.set_callback (parser)
		self.run_and_parse()

	def start(self, callback):
		self.set_cmd (self.cmd_start)
		self.set_callback (callback)
		self.run()

	def stop(self, callback):
		self.set_cmd (self.cmd_stop_Tor)
		self.set_callback (callback)
		self.run()
