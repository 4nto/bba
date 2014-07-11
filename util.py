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
'''
# AUTHOR Gabriele Lanaro
# https://pygabriel.wordpress.com/2009/07/27/redirecting-the-stdout-on-a-gtk-textview/
import gtk,glib
import subprocess
 
class CommandTextView(gtk.TextView):
    # Nice TextView that reads the output of a command syncronously
    def __init__(self, command):
        # command : the shell command to spawn
        super(CommandTextView, self).__init__()
        self.command = command
    def run(self):
        # Runs the process
        proc = subprocess.Popen(self.command, stdout = subprocess.PIPE) # Spawning
        glib.io_add_watch(proc.stdout, # file descriptor
                          glib.IO_IN,  # condition
                          self.write_to_buffer ) # callback
    def write_to_buffer(self, fd, condition):
        if condition == glib.IO_IN: #if there's something interesting to read
           char = fd.read(1) # we read one byte per time, to avoid blocking
           buf = self.get_buffer()
           buf.insert_at_cursor(char) # When running don't touch the TextView!!
           return True # FUNDAMENTAL, otherwise the callback isn't recalled
        else:
           return False # Raised an error: exit and I don't want to see you anymore
	'''           