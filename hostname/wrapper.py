import os
from util.batch import Batch
from __init__ import config

class Hostname(Batch):
    last = {'stdout': '', 'exit code': 0}
        
    def __init__(self, log, one_char_writer):
        self.log = log.getChild(__name__)
        Batch.__init__ (self, self.log)
        self.set_writer (one_char_writer)        

    def check (self, callback):
        def parser (exit_code, stdout):
            self.last['stdout'] = stdout 
            self.last['exit code'] = exit_code 
            self.msg = config.translate(str(exit_code)).format(stdout)
            callback (False if exit_code == 0 else True)
            
        self.set_cmd (config.get('cmd', 'check'), should_be_root = False)
        self.set_callback (parser)
        self.ipc_pipe_based()
        
    def reset (self, callback):
        self.set_callback (callback)
        self.set_cmd (config.get('cmd', 'set') + ' ' + self.last['stdout'])
        self.run()

    def randomize (self, callback):
        def random_callback (exit_code, stdout):
            random_name = stdout.strip()
            self.set_callback (callback)
            self.set_cmd (config.get('cmd', 'set') + ' ' + random_name)
            self.run()
                
        self.set_callback (random_callback) 
        self.set_cmd (config.get('cmd', 'random'), False)
        self.ipc_pipe_based()

    def set_script (self, script):
        pass
        
