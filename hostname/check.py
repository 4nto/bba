'''Get the last system startup hostname'''
import os, sys

log = '/var/log/kern.log'
checkline = "Linux version"

def lookup(fname, cnt = 0):
    if cnt > 0:
        fname = '{}.{}'.format(fname[:-2] if cnt > 1 else fname, cnt)       

    if not os.path.isfile(fname):
        sys.stderr.write("File or evidence not found\n")
        return
    
    with open(fname) as f:
        startup_lines = filter (lambda line: checkline in line, f)
        if len(startup_lines) == 0:
            lookup(fname, cnt + 1)
        else:
            try:
                init_hostname = startup_lines[-1].split()[3]
            except:
                sys.stderr.write("Parsing error\n")
            else:
                sys.stdout.write(init_hostname + '\n')

lookup(log)
