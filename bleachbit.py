from batch import Batch

class Bleachbit(Batch):
	cleaners = "bash.history system.cache system.clipboard system.custom system.recent_documents system.rotated_logs system.tmp system.trash"
#	cleaners = "bash.history"
	cmd_start = "bleachbit -o -c " + cleaners

	def __init__(self, log, output):		
		Batch.__init__ (self, self.cmd_start)
		self.set_new_writer (output)
		self.log = log

	def check(self, callback, seconds = 10):
		def parser (fd):
			callback ('Files to be deleted: 0' in fd.read()) # it works only in english !!!	

		self.set_cmd ("bleachbit -p -c " + self.cleaners, False)
		#self.set_new_writer (one_char_writer)
		self.set_callback (parser)
		self.run_and_parse()

	def get(self):
		return self.cleaners

	def set_no_overwrite(self):
		self.cmd_start = "bleachbit -c " + self.cleaners

	def set_overwrite(self):
		self.cmd_start = "bleachbit -o -c " + self.cleaners

	def start(self, callback):
		self.set_cmd (self.cmd_start)
		self.set_callback (callback)
		self.run()

