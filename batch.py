import subprocess, shlex, glib, os

class Batch():
	def __init__ (self, cmd, writer, callback = None):								
		self.set_cmd (cmd)
		self.set_writer (writer)
		self.set_callback (callback)

	def set_callback(self, callback):
		assert hasattr (callback, '__call__') if callback is not None else True
		self.callback = callback

	def set_cmd (self, cmd):
		assert isinstance (cmd, str) 
		self.cmd = shlex.split (cmd if os.geteuid() == 0 else "gksudo " + cmd)

	def set_writer (self, writer):
		assert hasattr (writer, '__call__') 
		self.writer = writer

	def run (self):
		proc = subprocess.Popen (self.cmd, stdout = subprocess.PIPE)
		glib.io_add_watch (proc.stdout, glib.IO_IN, self.writer)	
		glib.child_watch_add (proc.pid, self.callback)