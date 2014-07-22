
import netifaces as NI, re, subprocess, shlex, glib, os, urllib2
from socket import gethostname
from batch import Batch

class Hostname():
	rndname = None

	def __init__(self, LOG):
		self.log = lambda text: LOG.error(text)

	def check(self):
		proc = subprocess.Popen(['fgrep', 'Linux version', '/var/log/kern.log'], stdout=subprocess.PIPE)
		try:
			hostname_original = proc.stdout.readline()[:-1].split()[3]
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

	def random_hname(self):
		proc = subprocess.Popen(['shuf', '-n', '1', '/etc/dictionaries-common/words'], stdout=subprocess.PIPE)

class Clean:
	pass

def command_exist(fpath):
	return os.path.isfile(fpath) and os.access(fpath, os.X_OK)

'''
haridsv from stackoverflow
http://stackoverflow.com/questions/1714027/version-number-comparison
'''
def version_cmp(version1, version2):
    def normalize(v):
        return map (int, re.sub (r'(\.0+)*$','', v).split("."))
    return cmp (normalize(version1), normalize(version2))