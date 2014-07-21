
import netifaces, re, subprocess, shlex, glib, os, threading
from socket import gethostname

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
		pass

class Tor():
	def __init__(self, LOG):
		self.log = lambda text: LOG.error(text)

	def check(self):
		pass

	def start(self):
		pass

	def stop(self):
		pass


class NetworkInterfaces():
	def __init__(self, LOG):
		# check netifaces version
		# check macchanger
		self.pattern = re.compile(r"([0-9A-F]{2}[:-]){5}([0-9A-F]{2})", re.I)
		self.log = lambda text: LOG.error(text)
		self.update()

	def get_interfaces(self):
		return self.interfaces

	def get_default(self):
		return self.default_gw
		#return self.interfaces[0]
	
	def get_addr(self, ifname):
		return self.ifaddresses[ifname] if ifname in self.ifaddresses.keys() else None

	def get_number(self):
		return len(self.interfaces)

	def update(self):
		try:
			self.interfaces = netifaces.interfaces()
		except:
			self.log("Unable to obtain interfaces")
		try:
			self.ifaddresses = {iface:netifaces.ifaddresses(iface)[netifaces.AF_LINK][0]['addr'] for iface in self.interfaces}
		except:
			self.log("Unable to obtain interfaces addresses")
		try:
			self.default_gw = netifaces.gateways()['default'][netifaces.AF_INET][1] 
		except:
			self.log("Unable to obtain default gateway")

		self.ifspoofed = {iface:self.check_mac_address(iface) for iface in self.interfaces}		

	def is_spoofed(self, ifname):
		return self.ifspoofed[ifname] if ifname in self.ifspoofed.keys() else None

	def check_mac_address(self, iface):		
		proc = subprocess.Popen(['macchanger', '-s', iface], stdout=subprocess.PIPE)
		macs = map (lambda line: self.pattern.search(line).group(), proc.stdout)
		return macs[1:] == macs[:-1]

	# must be root
	def set_mac_address(self, iface):
		proc = subprocess.Popen(['macchanger', '-a', iface], stdout=subprocess.PIPE)
		return False if "ERROR" in proc.stdout else True

	#must be root
	def reset_mac_address(self, iface):
		proc = subprocess.Popen(['macchanger', '-p', iface], stdout=subprocess.PIPE)
		return False if "ERROR" in proc.stdout else True

class Clean:
	pass

class Batch():
	def __init__ (self, cmd, writer, callback = None):
		assert isinstance (cmd, str) 
		assert hasattr (writer, '__call__') 
		assert hasattr (self.callback, '__call__') if callback is not None else True

		self.cmd = shlex.split(cmd if os.geteuid() == 0 else "gksudo " + cmd)
		self.writer = writer
		self.callback = callback

	def run (self):
		proc = 	subprocess.Popen (self.cmd, stdout = subprocess.PIPE)
		glib.io_add_watch (proc.stdout, glib.IO_IN, self.writer)	
		glib.child_watch_add (proc.pid, self.my_callback)

		#if self.callback and hasattr (self.callback, '__call__'):
		#	proc.wait()
		#	self.callback()			

	def my_callback(self, first, second):
		self.writer("CALLBACK!!!")

class MyTask():
    def execute(self, my_task, on_task_complete):
        # executor = futures.ProcessPoolExecutor(max_workers=1)
        executor = futures.ThreadPoolExecutor(max_workers=1)
        future = executor.submit(self.my_task)
        future.add_done_callback(self.on_task_complete)

	def my_task(self):  
		LOG.debug("start my task")

	def on_task_complete(self, future):
		LOG.debug("on download task complete")

