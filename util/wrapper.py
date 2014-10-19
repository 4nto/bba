import os
from util.batch import Batch

class Wrapper(Batch):        
    def __init__(self, log, output, config):
        self.name = os.path.dirname(config.fname)
        self.log = log.getChild(self.name)
        Batch.__init__(self, self.log)
        self.set_writer(output)
        self.config = config
        self.output = output        

    def enable(self, enable_widget):
        '''
        VERIFY STEP
        Run in a separate process the verify script and if it returns no error then enables the related widget
        If there is no verify script enables the widget
        '''
        try:
            cmd = self.config.get('cmd', 'init')
        except:
            enable_widget()
            self.log.warning("No verify script for module {}".format(self.config.fname))
        else:
            def parser (exit_code, stdout):                 
                if exit_code == 0:
                    enable_widget()                        
                else:
                    self.output('Module "{}" disabled due to misconfiguration\n'.format(self.name))
            
            self.set_cmd(cmd, should_be_root = False)
            self.set_callback(parser)
            self.ipc_pipe_based(self.config.getint('config', 'timeout'))
        
    def check (self, callback):
        '''
        CHECK STEP
        Run in a separate process the check script, writes to gui console the stdout and according the exit code
        command the related widget
        '''
        def parser (exit_code, stdout):
            self.output(stdout)
            callback(True if exit_code == 0 else False)
            
        self.set_cmd(self.config.get('cmd', 'check'), should_be_root = False)
        self.set_callback(parser)
        self.ipc_pipe_based(self.config.getint('config', 'timeout'))

    def start (self, callback):
        self.set_callback(callback)
        self.set_cmd(self.config.get('cmd', 'start'))
        self.run(self.config.getint('config', 'timeout'))

    def stop (self, callback):
        self.set_callback(callback)
        self.set_cmd(self.config.get('cmd', 'stop'))
        self.run(self.config.getint('config', 'timeout'))
