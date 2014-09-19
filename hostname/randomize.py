'''Get a random name for the hostname'''
import os, sys, random

words = '/etc/dictionaries-common/words'

def randomize(fname):
    total_bytes = os.stat(fname).st_size
    with open(fname) as f:
        f.seek(random.randint(0, total_bytes))
        if f.readline() == "":
            randomize(fname)
        else:
            sys.stdout.write(f.readline())
        
randomize(words)
