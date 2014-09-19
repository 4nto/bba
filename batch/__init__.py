from gi.repository import GObject
import shlex
import os
#import tempfile
import signal
import io

class Batch(object):        
    def __init__ (self, log):
        self.log = log.getChild(__name__)
        self.envp = ['='.join(kv) for kv in os.environ.iteritems()]

    def set_callback(self, callback):
        assert hasattr (callback, '__call__')
        self.callback = callback

    def set_cmd (self, cmd, should_be_root=True):
        assert isinstance (should_be_root, bool)
        self.cmd = shlex.split ('gksudo "{}"'.format(cmd) if os.geteuid() != 0 and should_be_root else cmd)

    def run (self, mseconds = 0):
        assert hasattr (self, 'cmd') and hasattr (self, 'callback') and hasattr (self, 'writer')        
        pid, _, stdout, stderr = self.__run_spawn_async()        
        GObject.io_add_watch (stdout, GObject.IO_IN, self.writer)
        if mseconds > 0:
            timeout_id = GObject.timeout_add (mseconds, self.__timeout, pid)
            
        def callback_runner (*args):
            self.callback()
            self.__error_parser (stderr)
            if mseconds > 0:
                self.__timeout_remover (timeout_id)
        
        GObject.child_watch_add (pid, callback_runner)
        
    def ipc_pipe_based(self, mseconds = 0):
        assert hasattr (self, 'cmd') and hasattr (self, 'callback')        
        pid, _, stdout, stderr = self.__run_spawn_async()
        if mseconds > 0:
            timeout_id = GObject.timeout_add (mseconds, self.__timeout, pid)        
            
        def callback_parser (*args):
            with io.open(stdout) as fd:
                self.callback(fd)
            self.__error_parser (stderr)
            if mseconds > 0:
                self.__timeout_remover (timeout_id)            
              
        GObject.child_watch_add (pid, callback_parser)

    def ipc_file_based (self, mseconds = 0):
        assert hasattr (self, 'cmd') and hasattr (self, 'callback')
        self.cmd = ['python', 'batch/fprocess.py'] + self.cmd
        pid, _, stdout, stderr = self.__run_spawn_async()
        
        if mseconds > 0:
            timeout_id = GObject.timeout_add (mseconds, self.__timeout, pid)
            
        def callback_parser (*args):
            with io.open(stdout) as fd:
                with open(fd.read().strip()) as output:
                    self.callback(output)
                    
            self.__error_parser (stderr)
            if mseconds > 0:
                self.__timeout_remover (timeout_id)                     
                    
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
            os.kill (pid, signal.SIGKILL)
        except OSError:
            '''Already died'''
            pass
        else:
            self.log.warning ("command '{}' is taking too long, killed it".format(self.cmd[0]))
        finally:
            return False

    def __timeout_remover (self, source_id):        
        if not GObject.source_remove (source_id):
            '''Timeout was reached so there is not source_id yet'''
            pass
            # print "I'm not able to remove the error above :)"            
    
    def __run_spawn_async (self):
        return GObject.spawn_async (argv = self.cmd,
                                    envp = self.envp,
                                    flags = GObject.SPAWN_DO_NOT_REAP_CHILD|GObject.SPAWN_SEARCH_PATH,
                                    standard_output = True,
                                    standard_error = True)

    def __error_parser (self, stderr):
        with io.open(stderr) as fd:
            err = fd.read().strip()
            if err.strip() != "":
                self.log.error ("running '{}': {}".format(' '.join(self.cmd), err))
                    
