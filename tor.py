from batch import Batch
from util import command_exist

assert command_exist ("/usr/sbin/anonymous")

class Tor(Batch):
	cmd_start 	= '/sbin/anonymous start -t'
	cmd_stop 	= '/sbin/anonymous stop -t'
	cmd_check 	= 'curl -s https://check.torproject.org/?lang=en_US'

	def __init__(self, log, output):		
		Batch.__init__ (self, self.cmd_start)
		self.set_new_writer (output)
		self.log = log

	def check (self, callback, sec = 1):
		def parser (fd):
			checkline = lambda line: 'Congratulations. This browser is' in line
			callback (filter (checkline , fd.readlines()) != [])

		self.set_cmd (self.cmd_check, should_be_root = False)
		self.set_callback (parser)
		self.run_and_parse()

	def start(self):
		self.set_cmd (self.cmd_start)
		self.run()

	def stop(self):
		self.set_cmd (self.cmd_stop)
		self.run()
