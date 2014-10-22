'''Class to manage the multi-process batching architecture'''
from gi.repository import GObject
import signal
import shlex
import os
import io

class Batch(object):        
    def __init__ (self, log):
        self.log = log.getChild(__name__)
        self.envp = ['='.join(kv) for kv in os.environ.iteritems()]

    def set_callback(self, callback):
        assert hasattr (callback, '__call__')
        self.callback = callback

    def set_cmd (self, cmd):
        self.cmd = shlex.split (cmd)

    def run (self, mseconds = 0):
        assert hasattr (self, 'cmd') and hasattr (self, 'callback') and hasattr (self, 'writer')        
        pid, _, stdout, stderr = self.__run_spawn_async()        
        GObject.io_add_watch (stdout, GObject.IO_IN, self.writer)
        if mseconds > 0:
            timeout_id = GObject.timeout_add (mseconds, self.__timeout, pid)
            
        def callback_runner (*args):
            self.callback()
            with io.open(stderr) as err:
                self.__error_parser (err.read())
            if mseconds > 0:
                GObject.source_remove (timeout_id)
        
        GObject.child_watch_add (pid, callback_runner)
        
    def ipc_pipe_based(self, mseconds = 0):
        assert hasattr (self, 'cmd') and hasattr (self, 'callback')        
        pid, _, stdout, stderr = self.__run_spawn_async()
        if mseconds > 0:
            timeout_id = GObject.timeout_add (mseconds, self.__timeout, pid)        
            
        def callback_parser (*args):
            with io.open(stdout) as out, io.open(stderr) as err:
                self.callback((args[1] >> 8) & 0xFF, out.read())
                self.__error_parser (err.read())
              
            if mseconds > 0:
                GObject.source_remove (timeout_id)          
              
        GObject.child_watch_add (pid, callback_parser)
    
    def set_writer (self, one_char_writer):
        assert hasattr (one_char_writer, '__call__')
        
        def wrapped_writer (fd, condition):
            if condition == GObject.IO_IN:     	# if there's something interesting to read
                one_char_writer (os.read(fd, 1))     
                return True                 	# Continue to call this source

            return False			# Remove source

        self.writer = wrapped_writer

    def __timeout (self, pid):
        try:
            os.kill (pid, signal.SIGINT)
        except OSError:
            '''Already died'''
            pass
        else:
            self.log.warning ("command '{}' is taking too long, killed it".format(self.cmd[0]))
        finally:
            return False
    
    def __run_spawn_async (self):
        return GObject.spawn_async (argv = self.cmd,
                                    envp = self.envp,
                                    flags = GObject.SPAWN_DO_NOT_REAP_CHILD|GObject.SPAWN_SEARCH_PATH,
                                    standard_output = True,
                                    standard_error = True)

    def __error_parser (self, err):
        if err.strip() != "":
            self.log.error ("running '{}': {}".format(' '.join(self.cmd), err))
        
                    
