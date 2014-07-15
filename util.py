
import netifaces

class NetworkInterfaces:
	def __init__(self):
		self.interfaces = netifaces.interfaces()
		self.ifaddresses = {iface:netifaces.ifaddresses(iface)[netifaces.AF_LINK][0]['addr'] for iface in self.interfaces}
		self.default_gw = netifaces.gateways()['default'][netifaces.AF_INET][1]

	def get_interfaces(self):
		return self.interfaces

	def get_default(self):
		return self.default_gw
	
	def get_addr(self, ifname):
		if ifname not in self.interfaces:
			return None

		return self.ifaddresses[ifname]


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

