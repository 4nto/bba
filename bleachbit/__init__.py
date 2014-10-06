import sys
sys.path.append('.') 
from util.configuration import Configurator
from util import command_exist

config = Configurator('bleachbit/bleachbit.cfg')

assert command_exist (config.get('config', 'assert'))
