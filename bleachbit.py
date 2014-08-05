from batch import Batch
from util import command_exist

assert command_exist ("/usr/bin/bleachbit")

class Bleachbit(Batch):
#	cleaners = "bash.history system.cache system.clipboard system.custom system.recent_documents system.rotated_logs system.tmp system.trash"
	cleaners = "bash.history"
	cmd_start = "bleachbit -o -c " + cleaners

	def __init__(self, log, output):		
		Batch.__init__ (self, self.cmd_start)
		self.set_new_writer (output)
		self.log = log

	def check(self, callback, seconds = 10):
		def parser (fd):
			checkline = lambda line: 'Files to be deleted: 0' in line
			callback (filter (checkline , fd.readlines()) != []) # it works only in english !!!	

		self.set_cmd ("bleachbit -p -c " + self.cleaners, False)
		self.set_callback (parser)
		self.run_and_parse()

	def get(self):
		return self.cleaners

	def set_no_overwrite(self):
		self.set_cmd ("bleachbit -c " + self.cleaners)

	def set_overwrite(self):
		self.set_cmd ("bleachbit -o -c " + self.cleaners)

	def start(self):
		self.set_no_overwrite()
		self.run()

