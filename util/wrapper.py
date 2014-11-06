import os
from util.batch import Batch

class Wrapper(Batch):        
    def __init__(self, log, output, config, name):
        '''Wrapper class constructor'''
        self.name = name
        self.log = log.getChild(self.name)
        super(Wrapper, self).__init__(self.log)
        self.set_writer(output)
        self.config = config
        self.output = output
        
    '''
    VERIFY STEP
    (1) If it should be root and is root then move on
    (2) If there is no verify script then enables the widget
    (3) If the verify script returns with no errors then enables the widget
    '''
    def verify(self, enabling_widget):
        '''(1) Should be root?'''
        if self.config.getboolean('config', 'root') and os.geteuid() != 0:            
            '''self.output('Module "{}" must run as root\n'.format(self.name))'''
            ''' SHOW A WARNING'''
            enabling_widget(False)
            return

        '''(2) Is there the verify script?'''
        if not self.config.has_option('cmd', 'init'):            
            self.log.warning("No verify script")
            enabling_widget(True)
            return

        '''(3) Run the verify script'''
        def callback_verify_script (exit_code, stdout):                 
            if exit_code == 0:
                enabling_widget(True)                        
            else:
                self.output('Module "{}" disabled due to misconfiguration\n'.format(self.name))
                enabling_widget(False)
            
        self.set_cmd(self.config.get('cmd', 'init'))
        self.set_callback(callback_verify_script)
        self.ipc_pipe_based(self.config.getint('config', 'timeout'))
        
    '''
    CHECK STEP
    (1) Run in a separate process the check script
    (2) writes to gui console the stdout using a callback in the end of the proc
    (3) writes to log the stderr
    (4) according the exit code command the related widget
            True with 0, False instead
    '''        
    def check (self, callback):
        def parser (exit_code, stdout):
            self.output(stdout)
            callback(True if exit_code == 0 else False)
            
        self.set_cmd(self.config.get('cmd', 'check'))
        self.set_callback(parser)
        self.ipc_pipe_based(self.config.getint('config', 'timeout'))
    '''
    START/STOP STEP
    (1) Run in a separate process the start/stop script
    (2) writes to gui console the stdout in Real Time
    (3) writes to log the stderr
    '''
    def start (self, callback):
        self.set_callback(callback)
        self.set_cmd(self.config.get('cmd', 'start'))
        self.run(self.config.getint('config', 'timeout'))

    def stop (self, callback):
        self.set_callback(callback)
        self.set_cmd(self.config.get('cmd', 'stop'))
        self.run(self.config.getint('config', 'timeout'))
