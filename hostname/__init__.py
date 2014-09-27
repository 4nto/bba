import os
import socket
from batch import Batch
from util import command_exist

class Hostname(Batch):
    script_anonymous = 'anonymous'
    cmd_check = 'python hostname/check.py'
    cmd_random = 'python hostname/randomize.py'
    last_hostname = ''
    timeout = 30000 #30sec

    def __init__(self, log, one_char_writer):
        self.log = log.getChild(__name__)
        Batch.__init__ (self, self.log)
        self.set_writer (one_char_writer)        
        self.set_script(self.script_anonymous)

    def check (self, callback):
        def parser (exit_code, stdout):
            self.last_hostname = stdout
            if exit_code == 0:                
                self.msg = "Hostname {} is the same from the last boot".format(self.last_hostname)                
            elif exit_code == 1:
                self.msg = "Hostname {} is different from the last boot ({})".format(socket.gethostname(), self.last_hostname)
            else:
                self.msg = "Unable to retrieve your last boot hostname"
            
            callback (False if exit_code == 0 else True)
            
        self.set_cmd (self.cmd_check, should_be_root = False)
        self.set_callback (parser)
        self.ipc_pipe_based()
        
    def reset (self, callback):
        self.set_callback (callback)
        self.set_cmd (self.cmd_set + self.last_hostname)
        self.run()

    def randomize (self, callback):
        def random_callback (exit_code, stdout):
            random_name = stdout.strip()
            self.set_callback (callback)
            self.set_cmd (self.cmd_set + random_name)
            self.run()
                
        self.set_callback (random_callback) 
        self.set_cmd (self.cmd_random, False)
        self.ipc_pipe_based()

    def set_script (self, script):
        self.script_anonymous = script
        self.cmd_set = script + ' start -h '
        self.cmd_reset = script + ' stop -h '
        
