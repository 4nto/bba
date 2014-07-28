import subprocess, shlex, glib, os, sys

class Batch():
	def __init__ (self, cmd = None, writer = None, callback = None):		
		#self.log = lambda text: LOG.error(text)						
		self.cmd = cmd
		self.writer = writer
		self.callback = callback

	def set_callback(self, callback):
		assert hasattr (callback, '__call__')
		self.callback = callback

	def set_cmd (self, cmd, should_be_root=True):
		assert isinstance (cmd, str) and isinstance (should_be_root, bool)
		self.cmd = shlex.split ("gksudo " + cmd if os.geteuid() != 0 and should_be_root else cmd)

	def set_writer (self, writer):
		assert hasattr (writer, '__call__')
		self.writer = writer

	def run (self):
		try:
			proc = subprocess.Popen (self.cmd, stdout = subprocess.PIPE)
		except OSError:
			print "System-related error: '{}' does not seem to be a functional thing".format(self.cmd)
		except:
			print "Unexpected error:", sys.exc_info()[0]
		else:
			glib.io_add_watch (proc.stdout, glib.IO_IN, self.writer)	
			glib.child_watch_add (proc.pid, self.callback)
			return True

		return False

	def run_and_wait(self):
		proc = subprocess.Popen (self.cmd, stdout = subprocess.PIPE, stderr = subprocess.PIPE)
		return proc.communicate()
