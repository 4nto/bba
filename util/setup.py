'''
SETUP STEP
(1) If there is no module config file then move on
(2) If the config file syntax check is ok then move on
(3) if the config file dependencies are available but not satisfied then move on
(4) If there is no setup script then load the widget from the module config file
(5) If the setup script running completed successfully then create a
    widget for each config file returned
'''
import os
import ConfigParser
import util.batch 

def check_config(configurator):
    '''Verify the syntax of the config file'''
    required = (('config', 'title'), ('config', 'hide'), ('config', 'root'),
                ('config', 'timeout'), ('cmd', 'check'), ('cmd', 'start'))

    return all(map(lambda v: configurator.has_option(*v), required))

def check_dependences(dependences):
    '''Perform the check on the dependencies'''
    command_exist = lambda fpath: os.path.isfile(fpath) and os.access(fpath, os.X_OK)
    return all(map(command_exist, dependences.split(',')))  

def configure_module(module, load_widget_module, log):
    '''Perform the SETUP STEP for a single module'''
    log = log.getChild(module)
    setup = util.batch.Batch(log)      
    mconfig = ConfigParser.SafeConfigParser(allow_no_value = True)
    
    def run_setup_script(cmd):
        '''Run in background the setup script'''
        def setup_callback(exit_code, stdout):
            '''Callback launched at the end of the setup script'''
            if exit_code == 0:
                for line in stdout.splitlines():
                    dconfig = ConfigParser.SafeConfigParser(allow_no_value=True)
                    dconfig.read(line)
                    load_widget_module(module, dconfig)
            else:
                log.error("Error setting up the module:{}".format(stdout))
                
        setup.set_cmd(cmd, should_be_root = False)                    
        setup.set_callback(setup_callback)
        setup.ipc_pipe_based(mconfig.getint('config', 'timeout'))

    default_cfg_file = "{0}/{0}.cfg".format(module)
    
    if os.path.isfile(default_cfg_file):        
        mconfig.read(default_cfg_file)

        '''(2) Config file syntax check'''
        if not check_config(mconfig):
            log.error("Wrong configuration file")
            return
        
        '''(3) Config file dependencies'''
        if mconfig.has_option('config', 'assert') and not \
           check_dependences(mconfig.get('config', 'assert')):
            log.error("Unable to load module due to missing dependences")                                
            return

        '''(4,5) Run the setup script or load from the default config file'''
        if mconfig.has_option('config', 'setup'):                                    
            run_setup_script(mconfig.get('config', 'setup'))
        else:
            log.warning("No setup for module {}".format(module))                                     
            load_widget_module(module, mconfig) 
    else:
        log.error("No configuration file")
