from util.batch import Batch
from util.configuration import Configurator

class Wrapper(Batch):        
    def __init__(self, log, output, cfg):
        self.log = log.getChild(__name__)
        Batch.__init__ (self, self.log)
        self.set_writer (output)
        self.config = Configurator(cfg)
        self.last = {'stdout': '', 'exit code': 0}
        self.output = output
    
    def check (self, callback):
        def parser (exit_code, stdout):
            self.last['stdout'] = stdout 
            self.last['exit code'] = exit_code
            self.output(self.config.translate(str(exit_code)).format(stdout) + '\n')
            callback(True if exit_code == 0 else False)
            
        self.set_cmd(self.config.get('cmd', 'check'), should_be_root = False)
        self.set_callback(parser)
        self.ipc_pipe_based(self.config.getint('config', 'timeout'))

    def start (self, callback):
        self.set_callback(callback)
        self.set_cmd(self.config.get('cmd', 'start').format(self.last['stdout']))
        self.run(self.config.getint('config', 'timeout'))

    def stop (self, callback):
        self.set_callback(callback)
        self.set_cmd(self.config.get('cmd', 'stop').format(self.last['stdout']))
        self.run(self.config.getint('config', 'timeout'))

