import subprocess
import tempfile
import shlex
import sys

SIGINT_RECEIVED = "SIGINT received", 2
PARSING_ERROR = "Parsing error", 3

cleaners = "bash.history system.cache system.clipboard system.custom system.recent_documents system.rotated_logs system.tmp system.trash"
cmd_check = "/usr/bin/bleachbit -p -c {}".format(cleaners)
checkline = lambda line: 'Files to be deleted:' in line or 'File da eliminare:' in line


def check():
    output = subprocess.check_output(shlex.split(cmd_check))
    line = filter (checkline , output.split('\n'))

    if len(line) != 1:
        sys.stderr.write(PARSING_ERROR[0])
        return PARSING_ERROR[1]
 
    file_to_delete = line[0].split(':')[1].strip()
    sys.stdout.write(file_to_delete)
    return 0 if file_to_delete == '0' else 1

try:
    exit(check())
except KeyboardInterrupt:
    sys.stderr.write(SIGINT_RECEIVED[0])
    exit(SIGINT_RECEIVED[1])
except subprocess.CalledProcessError as e:
    pass
