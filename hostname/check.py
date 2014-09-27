'''Get the last system startup hostname'''
import os
import sys
import socket

SIGINT_RECEIVED = "SIGINT received", 2
FILE_NOT_FOUND = "File not found", 3
EVIDENCE_NOT_FOUND = "Evidence not found", 4
PARSING_ERROR = "Parsing error", 5

log = '/var/log/kern.log'
checkline = "Linux version"

def lookup(fname, cnt = 0):
    if cnt > 0:
        fname = '{}.{}'.format(fname[:-2] if cnt > 1 else fname, cnt)       

    if not os.path.isfile(fname):
        if cnt == 0:
            sys.stderr.write(FILE_NOT_FOUND[0])
            return FILE_NOT_FOUND[1]
        else:
            sys.stderr.write(EVIDENCE_NOT_FOUND[0])
            return EVIDENCE_NOT_FOUND[1]
    
    with open(fname) as f:
        startup_lines = filter (lambda line: checkline in line, f)
        if len(startup_lines) == 0:
            lookup(fname, cnt + 1)
        else:
            try:
                hostname = startup_lines[-1].split()[3]
            except:
                sys.stderr.write(PARSING_ERROR[0])
                return PARSING_ERROR[1]
            else:
                sys.stdout.write(hostname)
                return 0 if hostname == socket.gethostname() else 1

try:
    exit(lookup(log))
except KeyboardInterrupt:
    sys.stderr.write(SIGINT_RECEIVED[0])
    exit(SIGINT_RECEIVED[1])
