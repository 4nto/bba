import sys
sys.path.append('.') 
from configuration import Configurator
from util import command_exist

config = Configurator('bleachbit/bleachbit.cfg')

assert command_exist (config.get('config', 'assert'))
