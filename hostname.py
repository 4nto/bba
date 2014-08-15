import re
from socket import gethostname
from batch import Batch
from util import command_exist

assert command_exist ("/usr/sbin/anonymous")

class Hostname(Batch):
    startup_file = '/var/log/kern.log'   
    cmd_check = 'fgrep "Linux version" ' + startup_file
    cmd_random = 'shuf -n 1 /etc/dictionaries-common/words'
    cmd_set = '/usr/sbin/anonymous start -h '
    cmd_reset = '/usr/sbin/anonymous stop -h '
    timeout = 30000 #milliseconds

    def __init__(self, log, one_char_writer):
        self.log = log.getChild(__name__)
        Batch.__init__ (self, self.log)
        self.set_writer (one_char_writer)        
        self.pattern = re.compile (r"[a-z]*", re.I)

    ''' Get the system startup hostname '''
    def __startup_name (self, callback):
        def parser (fd):
            try:
                init_hostname = fd.readlines()[-1].split()[3]
            except:
                self.log.error ("Parsing error")
                callback (False)
            else:
                callback (init_hostname)

        self.set_cmd (self.cmd_check, should_be_root = False)
        self.set_callback (parser)
        self.run_and_parse()        

    def check (self, callback):
        def check_callback (init_hostname):
            callback (init_hostname != gethostname())

        self.__startup_name (check_callback)

    def reset (self, callback):
        def reset_callback (init_hostname):
            self.set_callback (callback)
            self.set (init_hostname)
            
        self.__startup_name (reset_callback)

    def set (self, hname):
        self.set_cmd (self.cmd_set + hname)
        self.run()

    def randomize (self, callback):
        def random_callback (random_raw_name):
            random_name = self.pattern.search(random_raw_name.readline()).group()

            if random_name.strip() == "":
                self.randomize (callback)
            else:    
                self.set_callback (callback)
                self.set (random_name.strip())

        self.set_callback (random_callback) 
        self.set_cmd (self.cmd_random, False)
        self.run_and_parse()
        
    def get(self):
        return gethostname()
    
