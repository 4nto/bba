from batch import Batch
from util import command_exist

class Tor(Batch):
    script_anonymous = 'anonymous'    
    cmd_check = 'python tor/check.py'
    timeout = 30000 #30sec
    
    def __init__(self, log, output):
        self.log = log.getChild(__name__)
        Batch.__init__ (self, self.log)
        self.set_writer (output)
        self.set_script(self.script_anonymous)
    
    def check (self, callback):
        def parser (exit_code, stdout):
            if exit_code == 0:
                self.msg = "Congratulation, you are using Tor as {}".format(stdout)
            elif exit_code == 1:
                self.msg = "Sorry but you {} are not using Tor".format(stdout)
            else:
                self.msg = "Unable to retrieve your IP"

            callback(True if exit_code == 0 else False)
            
        self.set_cmd (self.cmd_check, should_be_root = False)
        self.set_callback (parser)
        self.ipc_pipe_based(self.timeout)

    def start (self, callback):
        self.set_callback (callback)
        self.set_cmd (self.cmd_start)
        self.run()

    def stop (self, callback):
        self.set_callback (callback)
        self.set_cmd (self.cmd_stop)
        self.run()
        
    def set_script (self, script):
        self.script_anonymous = script
        self.cmd_start = script + ' start -t'
        self.cmd_stop = script + ' stop -t'
