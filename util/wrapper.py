import os
from util.batch import Batch

class Wrapper(Batch):
    '''
    This class commands a single modules
        * name:     the name of the module
        * output:   the function which writes on the textview normal data
        * check:    the function which writes on the textview check data
        * warning:  the function which writes on the textview warning data        
    '''
    def __init__(self, log, config, name, output, info, warning):
        '''Wrapper class constructor'''
        self.name = name
        self.log = log.getChild(self.name)
        self.config = config
        self.info = info
        self.warning = warning
        self.pid = None
        
        super(Wrapper, self).__init__(self.log)        
        self.set_writer(output)
        
        self.cwd = lambda cmd: './modules/{}/{}'.format(name, cmd)        
        self.start_cmd = self.cwd(self.config.get('cmd', 'start'))
        self.stop_cmd = self.cwd(self.config.get('cmd', 'stop'))
        self.check_cmd = self.cwd(self.config.get('cmd', 'check'))
        self.timeout = self.config.getint('config', 'timeout')
        
    '''
    VERIFY STEP
    (1) If it should be root and is root then move on
    (2) If there is no verify script then enables the widget
    (3) If the verify script returns with no errors then enables the widget
    '''
    def verify(self, enabling_widget):
        '''(1) Should be root?'''
        if self.config.getboolean('config', 'root') and os.geteuid() != 0:            
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
                self.warning('Module "{}" disabled: {}\n'.format(self.name,
                                                                stdout.strip()))
                enabling_widget(False)

        cmd = self.cwd(self.config.get('cmd', 'init'))
        self.set_cmd(cmd)
        self.set_callback(callback_verify_script)
        self.ipc_pipe_based(self.timeout)
        
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
            self.info(stdout)
            callback(True if exit_code == 0 else False)
            
        self.set_cmd(self.check_cmd)
        self.set_callback(parser)
        self.ipc_pipe_based(self.timeout)
    '''
    START/STOP STEP
    (1) Run in a separate process the start/stop script
    (2) writes to gui console the stdout in Real Time
    (3) writes to log the stderr
    '''
    def start (self, callback):
        self.set_callback(callback)
        self.set_cmd(self.start_cmd)
        self.pid = self.run(self.timeout)

    def stop (self, callback):
        self.set_callback(callback)
        self.set_cmd(self.stop_cmd)
        self.pid = self.run(self.timeout)

    '''
    Kill a running process
    '''
    def halt(self, user_data):
        if self.pid:
            self.kill(self.pid)
