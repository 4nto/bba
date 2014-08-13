from gi.repository import GObject
import shlex, os, tempfile

class Batch(object):        
    def __init__ (self):
        self.envp = ['='.join(kv) for kv in os.environ.iteritems()]

    def set_callback(self, callback):
        assert hasattr (callback, '__call__')
        self.callback = callback

    def set_cmd (self, cmd, should_be_root=True):
        assert isinstance (cmd, str) and isinstance (should_be_root, bool)
        self.cmd = shlex.split ('gksudo "{}"'.format(cmd) if os.geteuid() != 0 and should_be_root else cmd)

    def run (self):
        assert hasattr (self, 'cmd') and hasattr (self, 'callback') and hasattr (self, 'writer')        
        pid, _, stdout, stderr = self.__run_spawn_async()        
        GObject.io_add_watch (stdout, GObject.IO_IN, self.writer)
        
        def callback_runner (*args):
            self.callback()
            self.__error_parser (stderr)
        
        GObject.child_watch_add (pid, callback_runner) 
        
    def run_and_parse(self):
        assert hasattr (self, 'cmd') and hasattr (self, 'callback')        
        pid, _, stdout, stderr = self.__run_spawn_async()
                        
        def callback_parser (*args):
            with os.fdopen(stdout) as fd:
                self.callback(fd)
            self.__error_parser (stderr)            
              
        GObject.child_watch_add (pid, callback_parser)

    def __run_spawn_async (self):
        return GObject.spawn_async (argv = self.cmd,
                                    envp = self.envp,
                                    flags = GObject.SPAWN_DO_NOT_REAP_CHILD|GObject.SPAWN_SEARCH_PATH,
                                    standard_output = True,
                                    standard_error = True)

    def __error_parser (self, stderr):
        with os.fdopen(stderr) as fd:
            err = fd.read()
            if err.strip() != "":
                print "ERROR RUNNING COMMAND {}:".format(self.cmd[0])
                print err.strip()
                    
    def set_writer (self, one_char_writer):
        assert hasattr (one_char_writer, '__call__')
        
        def wrapped_writer (fd, condition):
            if condition == GObject.IO_IN:     	# if there's something interesting to read
                one_char_writer (os.read(fd, 1))     
                return True                 	# FUNDAMENTAL, otherwise the callback isn't recalled

            return False			# Raised an error: exit and I don't want to see you anymore 

        self.writer = wrapped_writer
