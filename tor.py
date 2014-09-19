import re
from batch import Batch
from util import command_exist

assert command_exist ("anonymous")

class Tor(Batch):
    script_anonymous = 'anonymous'    
    cmd_check = 'curl -s https://check.torproject.org/?lang=en_US'
    timeout = 30000 #milliseconds
    IP = 'n/a'
    
    def __init__(self, log, output):
        self.log = log.getChild(__name__)
        Batch.__init__ (self, self.log)
        self.set_writer (output)
        self.checkline = lambda line: 'Congratulations. This browser is' in line
        self.set_script(self.script_anonymous)
        self.pattern = re.compile (r'[0-9]+(?:\.[0-9]+){3}', re.I)
        
    def check (self, callback):
        def parser (fd):
            lines = fd.readlines()
            IPline = filter(lambda line: "IP address" in line, lines)
            self.IP = self.pattern.search(IPline[0]).group() if len(IPline) == 1 else 'n/a'
            callback (filter (self.checkline, lines) != [])

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
