import subprocess
import tempfile
import sys

with tempfile.NamedTemporaryFile(mode='w', prefix='bba_', delete=False) as f:
    try:    
        f.write(subprocess.check_output(sys.argv[1:]))
    except:
        sys.stderr.write("Error in execution of {}".format(sys.argv[1:]))
    else:
        sys.stdout.write(f.name)
