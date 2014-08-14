from batch import Batch
from util import command_exist

assert command_exist ("/usr/sbin/anonymous")

class Tor(Batch):
    cmd_start   = '/usr/sbin/anonymous start -t'
    cmd_stop    = '/usr/sbin/anonymous stop -t'
    cmd_check   = 'curl -s https://check.torproject.org/?lang=en_US'        
    
    def __init__(self, log, output):
        self.log = log.getChild(__name__)
        Batch.__init__ (self, self.log)
        self.set_writer (output)
        self.checkline = lambda line: 'Congratulations. This browser is' in line
        
    def check (self, callback, sec = 1):
        def parser (fd):
            self.log.error ("test parsing!")
            callback (filter (self.checkline, fd.readlines()) != [])

        self.set_cmd (self.cmd_check, should_be_root = False)
        self.set_callback (parser)
        self.run_and_parse()

    def start(self, callback):
        self.set_callback (callback)
        self.set_cmd (self.cmd_start)
        self.run()

    def stop(self, callback):
        self.set_callback (callback)
        self.set_cmd (self.cmd_stop)
        self.run()
