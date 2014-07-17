
import netifaces, re, subprocess

class NetworkInterfaces:
	def __init__(self):
		self.pattern = re.compile(r"([0-9A-F]{2}[:-]){5}([0-9A-F]{2})", re.I)
		self.interfaces = netifaces.interfaces()
		self.ifaddresses = {iface:netifaces.ifaddresses(iface)[netifaces.AF_LINK][0]['addr'] for iface in self.interfaces}
		self.default_gw = netifaces.gateways()['default'][netifaces.AF_INET][1]
		self.ifspoofed = {iface:self.check_current_mac_address(iface) for iface in self.interfaces}

	def get_interfaces(self):
		return self.interfaces

	def get_default(self):
		return self.default_gw
	
	def get_addr(self, ifname):
		return self.ifaddresses[ifname] if ifname in self.ifaddresses.keys() else None

	def get_number(self):
		return len(self.interfaces)

	def update(self):
		self.__init__()

	def is_spoofed(self, ifname):
		return self.ifspoofed[ifname] if ifname in self.ifspoofed.keys() else None

	def check_current_mac_address(self, iface):		
		proc = subprocess.Popen(['macchanger', '-s', iface], stdout=subprocess.PIPE)
		macs = map (lambda line: self.pattern.search(line).group(), proc.stdout)
		return macs[1:] == macs[:-1]

class MyTask():
    def execute(self):
        # executor = futures.ProcessPoolExecutor(max_workers=1)
        executor = futures.ThreadPoolExecutor(max_workers=1)
        future = executor.submit(self.my_task)
        future.add_done_callback(self.on_task_complete)

	def my_task(self):  
		LOG.debug("start my task")

	def on_task_complete(self, future):
		LOG.debug("on download task complete")

