#!/usr/bin/env python
'''Setup the bleachbit config file'''
from __future__ import print_function
import ConfigParser
import tempfile
import sys
import os

def setup(module):
    config = ConfigParser.SafeConfigParser()

    bleachbit_cfg = os.path.expanduser("~") + '/.config/bleachbit/bleachbit.ini'
    if not os.path.isfile(bleachbit_cfg):
        '''There is no bleachbit configuration file'''
        return

    config.read(bleachbit_cfg)
    if config.has_section('preserve_languages') \
       and config.has_option('preserve_languages', 'en') \
       and config.getboolean('preserve_languages', 'en'):

        op = 'Files deleted'
        check = 'Files to be deleted'
        
    else:        
        raise Exception('Unable to check Bleachbit used language')
    
    config.read('{}.cfg'.format(module))
    config.set('config', 'pattern_op', op)
    config.set('config', 'pattern_check', check)
    
    with tempfile.NamedTemporaryFile(prefix = module, delete = False) as fd:
        config.write(fd)

    print(fd.name)    

try:
    os.chdir(os.path.dirname(__file__))
    setup(os.path.abspath(__file__).split('/')[-2])
    
except KeyboardInterrupt:
    print("SIGINT received (timeout or CTRL+C)", file=sys.stderr)
    sys.exit(1)
    
except Exception as inst:
    print("Unknown_error: {}".format(inst), file=sys.stderr)
    sys.exit(1)
