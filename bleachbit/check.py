import subprocess
import signal
import shlex
import sys
import os

from __init__ import config

cmd_check = config.get('config', 'check')

def check(proc):
    checkline = lambda line: 'Files to be deleted:' in line or 'File da eliminare:' in line
    (output, error) = proc.communicate()
    line = filter (checkline, output.splitlines())

    try: 
        file_to_delete = line[0].split(':')[1].strip()
    except:
        config.exit_with_error('parsing_error')
        
    sys.stdout.write(file_to_delete)
    if file_to_delete != '0':
       config.exit_with_error('ko') 

try:
    proc = subprocess.Popen(shlex.split(cmd_check), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    check(proc)
except KeyboardInterrupt:
    os.kill(proc.pid, signal.SIGTERM)
    config.exit_with_error('sigint_received')
#except subprocess.CalledProcessError as e:
#    pass
