import os
from socket import gethostname
from batch import Batch
from util import command_exist

assert command_exist ("anonymous")

class Hostname(Batch):
    script_anonymous = 'anonymous'
    cmd_check = 'python hostname/check.py'
    cmd_random = 'python hostname/randomize.py'
    last_hostname = 'n/a'
    timeout = 30000 #30sec

    def __init__(self, log, one_char_writer):
        self.log = log.getChild(__name__)
        Batch.__init__ (self, self.log)
        self.set_writer (one_char_writer)        
        self.set_script(self.script_anonymous)

    def check (self, callback):
        def parser (fd):
            self.last_hostname = fd.read().strip()
            callback (self.last_hostname != gethostname())

        self.set_cmd (self.cmd_check, should_be_root = False)
        self.set_callback (parser)
        self.ipc_pipe_based()
        
    def reset (self, callback):
        self.set_callback (callback)
        self.set_cmd (self.cmd_set + self.last_hostname)
        self.run()

    def randomize (self, callback):
        def random_callback (fd):
            random_name = fd.read().strip()
            self.set_callback (callback)
            self.set_cmd (self.cmd_set + random_name)
            self.run()
                
        self.set_callback (random_callback) 
        self.set_cmd (self.cmd_random, False)
        self.ipc_pipe_based()
        
    def get(self):
        return gethostname()

    def set_script (self, script):
        self.script_anonymous = script
        self.cmd_set = script + ' start -h '
        self.cmd_reset = script + ' stop -h '
        
