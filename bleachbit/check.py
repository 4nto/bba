import subprocess
import signal
import shlex
import sys
import os

SIGINT_RECEIVED = "SIGINT received (timeout or CTRL+C)", 2
PARSING_ERROR = "Parsing error", 3

cleaners = "bash.history system.cache system.clipboard system.custom system.recent_documents system.rotated_logs system.tmp system.trash"
cmd_check = "/usr/bin/bleachbit -p -c {}".format(cleaners)
checkline = lambda line: 'Files to be deleted:' in line or 'File da eliminare:' in line

def check(proc):
    (output, error) = proc.communicate()
    line = filter (checkline , output.splitlines())

    if len(line) != 1:
        sys.stderr.write(PARSING_ERROR[0])
        return PARSING_ERROR[1]
 
    file_to_delete = line[0].split(':')[1].strip()
    sys.stdout.write(file_to_delete)
    return 0 if file_to_delete == '0' else 1

#if __name__ == '__main__':

try:
    proc = subprocess.Popen(shlex.split(cmd_check), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    sys.exit(check(proc))
except KeyboardInterrupt:
    os.kill(proc.pid, signal.SIGTERM)
    sys.stderr.write(SIGINT_RECEIVED[0])
    sys.exit(SIGINT_RECEIVED[1])
#except subprocess.CalledProcessError as e:
#    pass
