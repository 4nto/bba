#!/usr/bin/env python

import subprocess
import tempfile
import sys

with tempfile.NamedTemporaryFile(mode='w', prefix='bba_', delete=False) as f:
    try:    
        f.write(subprocess.check_output(sys.argv[1:]))
    except:
        print "Error in execution of {}".format(sys.argv[1:])
    else:
        print f.name
