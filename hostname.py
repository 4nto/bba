import re
from socket import gethostname

from batch import Batch

class Hostname(Batch):
	rndname = None
	cmd_check = 'fgrep "Linux version" /var/log/kern.log'
	cmd_random = 'shuf -n 1 /etc/dictionaries-common/words'
	cmd_set = 'sh ../backbox-anonymous/usr/sbin/anonymous start -h '
	cmd_reset = 'sh ../backbox-anonymous/usr/sbin/anonymous stop -h '

	def __init__(self, log, one_char_writer):
		Batch.__init__ (self)
		self.set_new_writer (one_char_writer)
		self.log = log

	def get_previous_name(self):
		self.set_cmd (self.cmd_check, False)
		result = self.run_and_wait()[0].strip()
		try:
			hostname_original = result.split('\n')[-1].split()[3]
		except:
			self.log("Unable to open kern.log or parsing it")
			return ""
		else:
			return hostname_original

	def check(self, arg = None):
		return gethostname() != self.get_previous_name()	

	def get(self):
		return gethostname()

	def reset(self):
		hostname_original = self.get_previous_name()
		if hostname_original != "":
			self.set (hostname_original)
		else:
			#map (one_char_writer, "Unable to find a previous hostname\n")
			self.log ("Unable to find a previous hostname")

	def set(self, hname):
		self.set_cmd (self.cmd_set + hname)
		self.run()

	def random(self):
		self.set_cmd (self.cmd_random, False)
		result = self.run_and_wait()[0].strip().lower()
		return re.match('[a-z]*', result).group()
		
