'''Check the current mac addr'''
import subprocess
import shlex
import sys
import re

sys.path.append('.') 
from util.configuration import Configurator
config = Configurator('network/network.cfg')

if len(sys.argv) != 2:
    config.exit_with_error('arguments_error') 

def check(proc):
    pattern = re.compile (r"([0-9A-F]{2}[:-]){5}([0-9A-F]{2})", re.I)
    (stdout, stderr) = proc.communicate()
    try:
        macs = map (lambda line: pattern.search(line).group(), stdout.strip().splitlines())
    except:
        config.exit_with_error('parsing_error') 
    else:
        sys.stdout.write(macs[:-1][0])
        
        if macs[1:] == macs[:-1]:
            config.exit_with_error('ko') 

try:
    proc = subprocess.Popen(shlex.split("macchanger -s {}".format(sys.argv[1])), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    check(proc)
except KeyboardInterrupt:
    config.exit_with_error('sigint_received')
