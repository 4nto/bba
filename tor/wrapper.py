from batch import Batch
from __init__ import config

class Tor(Batch):
    last = {'stdout': '', 'exit code': 0}
    
    def __init__(self, log, output):
        self.log = log.getChild(__name__)
        Batch.__init__ (self, self.log)
        self.set_writer (output)
    
    def check (self, callback):
        def parser (exit_code, stdout):
            self.last['stdout'] = stdout 
            self.last['exit code'] = exit_code             
            self.msg = config.translate(str(exit_code)).format(stdout)
            callback(True if exit_code == 0 else False)
            
        self.set_cmd (config.get('cmd', 'check'), should_be_root = False)
        self.set_callback (parser)
        self.ipc_pipe_based(config.getint('config', 'timeout'))

    def start (self, callback):
        self.set_callback (callback)
        self.set_cmd (config.get('cmd', 'start'))
        self.run()

    def stop (self, callback):
        self.set_callback (callback)
        self.set_cmd (config.get('cmd', 'stop'))
        self.run()
        
    def set_script (self, script):
        pass
