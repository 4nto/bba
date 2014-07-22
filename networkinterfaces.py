import re, subprocess, pkg_resources
import netifaces as NI
from batch import Batch
from util import version_cmp, command_exist

# netifaces version must be greater than 0.10.4
assert version_cmp (pkg_resources.get_distribution("netifaces").version, "0.10.4") >= 0
assert command_exist ("/usr/bin/macchanger")

class NetworkInterfaces(Batch):
	def __init__(self, LOG, output):
		Batch.__init__ (self, "macchanger -h", output)
		self.pattern = re.compile(r"([0-9A-F]{2}[:-]){5}([0-9A-F]{2})", re.I)
		self.log = lambda text: LOG.error(text)
		self.update()

	def update(self):
		try:	self.interfaces = NI.interfaces()
		except:	self.log("Unable to obtain interfaces")

		try:	self.ifaddresses = {i:NI.ifaddresses(i)[NI.AF_LINK][0]['addr'] for i in self.interfaces}
		except:	self.log("Unable to obtain interfaces addresses")

		try:	self.default_gw = NI.gateways()['default'][NI.AF_INET][1] 
		except:	self.log("Unable to obtain default gateway")

		self.ifspoofed = {iface:self.check(iface) for iface in self.interfaces}	

	def get_interfaces(self): 	return self.interfaces
	def get_default(self): 		return self.default_gw #return self.interfaces[0]
	def get_number(self):		return len(self.interfaces)	
	def get_addr(self, iname):	return self.ifaddresses[iname] if iname in self.ifaddresses.keys() else None		

	def is_spoofed(self, ifname):
		return self.ifspoofed[ifname] if ifname in self.ifspoofed.keys() else None

	def check(self, iface):		
		proc = subprocess.Popen(['macchanger', '-s', iface], stdout=subprocess.PIPE)
		macs = map (lambda line: self.pattern.search(line).group(), proc.stdout)
		return macs[1:] == macs[:-1]

	def set(self, iface, callback):
		print "GOING TO SET " + iface + " ADDR: macchanger -a {}".format (iface)
		self.set_cmd ("macchanger -a {}".format (iface))
		self.set_callback (callback)
		self.run()

	def reset(self, iface, callback):
		self.set_cmd ("macchanger -p {}".format (iface))
		self.set_callback (callback)
		self.run()