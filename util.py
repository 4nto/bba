from netifaces import interfaces, ifaddresses, AF_LINK

class NetworkInterfaces:
	def __init__(self):
		pass

	def get_interfaces(self):
		return interfaces()

	def get_addr(self, ifname):
		if ifname not in interfaces():
			print "Brutta storia"
			return None

		return ifaddresses(ifname)[AF_LINK][0]['addr']


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
