from batch import Batch
from util import command_exist

assert command_exist ("/usr/bin/bleachbit")

class Bleachbit(Batch):
	cleaners = "bash.history system.cache system.clipboard system.custom system.recent_documents system.rotated_logs system.tmp system.trash"
#	cleaners = "bash.history system.cache system.clipboard"
	cmd_start = "/usr/bin/bleachbit -c " + cleaners
	cmd_start_overwrite = "/usr/bin/bleachbit -o -c " + cleaners
	cmd_check = "/usr/bin/bleachbit -p -c '{}'".format(cleaners)
	timeout = 30000 #milliseconds

	def __init__(self, log, output):
                self.log = log.getChild(__name__)
		Batch.__init__ (self, self.log)		
		self.set_writer (output)
		self.set_no_overwrite()

	def check(self, callback):
		def parser (fd):
			checkline = lambda line: 'Files to be deleted: 0' in line or 'File eliminati: 0' in line
			callback (filter (checkline , fd.readlines()) != []) # it works only in english !!!	

		self.set_cmd (self.cmd_check, False)
		self.set_callback (parser)
		self.run_and_parse(self.timeout)

	def get(self):
		return self.cleaners

	def set_no_overwrite(self):
		self.set_cmd (self.cmd_start, False)

	def set_overwrite(self):
		self.set_cmd (self.cmd_start_overwrite, False)

	def start(self, callback):
                self.set_no_overwrite()
                self.set_callback (callback)
		self.run(self.timeout)

