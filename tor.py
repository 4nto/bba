import urllib2
from batch import Batch

class Tor(Batch):
	cmd_start_Tor = "sh ./test.sh"

	def __init__(self, LOG, output):		
		Batch.__init__ (self, self.cmd_start_Tor, output)
		self.log = lambda text: LOG.error(text)

	def check(self):
		html = urllib2.urlopen('https://check.torproject.org/?lang=en_US').read()
		return True if "Congratulations. This browser is" in html else False

	def start(self, callback):
		self.set_cmd (self.cmd_start_Tor)
		self.set_callback (callback)
		self.run()

	def stop(self, callback):
		self.set_cmd (self.cmd_stop_Tor)
		self.set_callback (callback)
		self.run()