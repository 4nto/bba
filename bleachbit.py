from batch import Batch
from util import command_exist

assert command_exist ("/usr/bin/bleachbit")

class Bleachbit(Batch):
    cleaners = "bash.history system.cache system.clipboard system.custom system.recent_documents system.rotated_logs system.tmp system.trash"
#   cleaners = "bash.history system.cache system.clipboard"
    cmd_start = "/usr/bin/bleachbit -c {}".format(cleaners)
    cmd_start_overwrite = "/usr/bin/bleachbit -o -c {}".format(cleaners)
    cmd_check = "/usr/bin/bleachbit -p -c {}".format(cleaners)
    timeout = 60000 #60sec 
    file_to_delete = "n/a"

    def __init__(self, log, output):
        self.log = log.getChild(__name__)
        Batch.__init__ (self, self.log)     
        self.set_writer (output)
        self.set_no_overwrite()
        self.checkline = lambda line: 'Files to be deleted' in line or 'File da eliminare' in line

    def check(self, callback):
        def parser (fd):
            line = filter (self.checkline , fd)
            try:
                self.file_to_delete = line[0].split(':')[1].strip() 
            except:
                self.file_to_delete = "n/a"
            callback ( line != []) # it works only in english !!!
                        
        self.set_cmd (self.cmd_check, False)
        self.set_callback (parser)
        self.ipc_file_based(self.timeout)
        
    def get(self):
        return self.cleaners

    def set_no_overwrite(self):
        self.set_cmd (self.cmd_start, False)

    def set_overwrite(self):
        self.set_cmd (self.cmd_start_overwrite, False)

    def start(self, callback):
        self.set_no_overwrite()
        self.set_callback (callback)
        self.run(self.timeout)

