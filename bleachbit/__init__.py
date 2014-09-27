from batch import Batch
from util import command_exist

assert command_exist ("/usr/bin/bleachbit")

class Bleachbit(Batch):
    cleaners = "bash.history system.cache system.clipboard system.custom system.recent_documents system.rotated_logs system.tmp system.trash"
    cmd_start = "/usr/bin/bleachbit -c {}".format(cleaners)
    cmd_start_overwrite = "/usr/bin/bleachbit -o -c {}".format(cleaners)
    cmd_check = 'python bleachbit/check.py'
    timeout = 60000 #60sec 
    file_to_delete = "n/a"

    def __init__(self, log, output):
        self.log = log.getChild(__name__)
        Batch.__init__ (self, self.log)     
        self.set_writer (output)
        self.set_no_overwrite()
        self.checkline = lambda line: 'Files to be deleted' in line or 'File da eliminare' in line

    def check(self, callback):
        def parser (exit_code, stdout):
            if exit_code == 0:
                self.msg = "Your system is clean"
            elif exit_code == 1:
                self.msg = "There are {} files to remove".format(stdout)
            else:
                self.msg = "Unable to verify your data"

            callback(True if exit_code == 0 else False)
            
        self.set_cmd (self.cmd_check, False)
        self.set_callback (parser)
        self.ipc_pipe_based(self.timeout)        
        
    def get(self):
        return self.cleaners

    def set_no_overwrite(self):
        self.set_cmd (self.cmd_start)

    def set_overwrite(self):
        self.set_cmd (self.cmd_start_overwrite)

    def start(self, callback):
        self.set_no_overwrite()
        self.set_callback (callback)
        self.run(self.timeout)

