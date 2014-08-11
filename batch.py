# Thanks to Alex Martelli from stackoverflow.com/questions/1191374

from gi.repository import GObject
import subprocess, shlex, os, tempfile

import time

class Batch(object):        
    def __init__ (self):
        self.spawn_flags = GObject.SPAWN_DO_NOT_REAP_CHILD|GObject.SPAWN_SEARCH_PATH
        self.envp = ['='.join(kv) for kv in os.environ.iteritems()]
        #self.original = lambda: map(self.cmd)
        pass

    def set_callback(self, callback):
        assert hasattr (callback, '__call__')
        self.callback = callback

    def set_cmd (self, cmd, should_be_root=True):
        assert isinstance (cmd, str) and isinstance (should_be_root, bool)
        self.cmd = shlex.split ('gksudo "{}"'.format(cmd) if os.geteuid() != 0 and should_be_root else cmd)

    def run (self):
        assert hasattr (self, 'cmd') and hasattr (self, 'callback') and hasattr (self, 'writer')
        try:
                proc = subprocess.Popen (self.cmd, stdout = subprocess.PIPE)
        except OSError:
                print "System-related error: '{}' does not seem to be a functional thing".format(self.cmd)
        else:
                GObject.io_add_watch (proc.stdout, GObject.IO_IN, self.writer)	
                GObject.child_watch_add (proc.pid, self.callback)

    def run_new (self):
        assert hasattr (self, 'cmd') and hasattr (self, 'callback') and hasattr (self, 'writer')
        pid, _, fd, _ = GObject.spawn_async (self.cmd, envp = self.envp, flags = self.spawn_flags, standard_output=True)
        GObject.io_add_watch (os.fdopen(fd), GObject.IO_IN, self.writer)    
        GObject.child_watch_add (pid, self.callback) 
        
    def run_and_parse(self):
        assert hasattr (self, 'cmd') and hasattr (self, 'callback')
        pid, _, fd, _ = GObject.spawn_async (self.cmd, envp = self.envp, flags = self.spawn_flags, standard_output=True)
                        
        def callback_parser (*args):
            with os.fdopen(fd) as fo:
                self.callback(fo)
              
        GObject.child_watch_add (pid, callback_parser)		

    def set_writer(self, one_char_writer):
        assert hasattr (one_char_writer, '__call__')
        
        def wrapped_writer(fd, condition, one_char_writer):
            if condition == GObject.IO_IN:     	# if there's something interesting to read
                one_char_writer (fd.read(1))    # we read one byte per time, to avoid blocking
                return True                 	# FUNDAMENTAL, otherwise the callback isn't recalled

            return False			# Raised an error: exit and I don't want to see you anymore 

        self.writer = lambda fd, condition: wrapped_writer (fd, condition, one_char_writer)

'''
    def run_and_wait(self, timeout = 3):
        try:
            proc = subprocess.Popen (self.cmd, stdout = subprocess.PIPE, stderr = subprocess.PIPE)
        except OSError:
            print "System-related error: '{}' does not seem to be a functional thing".format(self.cmd[0] + " (...)")
        else:						
            try:
                with Timeout (timeout):
                    return proc.communicate()
            except Timeout.Timeout:
                print "\"{}\" execution is taking longer than {}!".format(self.cmd[0] + " (...)", timeout)	
                proc.terminate()				

        return (None, None)

class Timeout():
    class Timeout(Exception): pass

    def __init__(self, sec):
            self.sec = sec

    def __enter__(self):
            signal.signal(signal.SIGALRM, self.raise_timeout)
            signal.alarm(self.sec)

    def __exit__(self, *args):
            signal.alarm(0) # disable alarm

    def raise_timeout(self, *args):
            raise Timeout.Timeout()

'''
