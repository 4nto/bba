import re
from socket import gethostname

from batch import Batch

class Hostname(Batch):
	rndname = None
	cmd_check = 'fgrep "Linux version" /var/log/kern.log'
	cmd_random = 'shuf -n 1 /etc/dictionaries-common/words'

	def __init__(self, LOG):
		Batch.__init__ (self)
		self.log = lambda text: LOG.error(text)

	def check(self):
		self.set_cmd (self.cmd_check, False)
		result = self.run_and_wait()[0].strip()
		try:
			hostname_original = result.split('\n')[-1].split()[3]
		except:
			self.log("Unable to open kern.log or parsing it")
			return True

		return gethostname() == hostname_original	

	def get(self):
		return gethostname()

	def reset(self):
		pass

	def set(self, hname=rndname):
		pass

	def random(self):
		self.set_cmd (self.cmd_random, False)
		result = self.run_and_wait()[0].strip().lower()
		return re.match('[a-z]*', result).group()
		
