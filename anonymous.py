import os
import shlex
import shutil
import subprocess
'''
class process():
    def __init__(self, cmd):
        proc = subprocess.Popen(shlex.split(cmd), stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    def __enter__(self):
        return proc.communicate()

    def __exit__(self):
        os.kill(proc.pid)
'''
def clean_dhcp():    
    proc = subprocess.Popen(shlex.split("dhclient -r"), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    (output, error) = proc.communicate()
    shutil.rmtree('/var/lib/dhcp/')


def service(name, op):
    if op not in ('start', 'stop', 'restart'):
        return False

    cmd = "service {} {}".format(name, op)
    proc = subprocess.Popen(shlex.split(cmd), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
