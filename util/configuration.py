import os
import sys
import ConfigParser

class Configurator(ConfigParser.SafeConfigParser):
    def __init__(self, fname):
        ConfigParser.SafeConfigParser.__init__(self, allow_no_value = True)
        self.read(fname)
        self.fname = fname

    def translate(self, code):
        match = filter(lambda c: c[1] == code, self.items('code'))
        return self.get('application_msg', match[0][0])
    
    def exit_with_error(self, error):
        sys.stderr.write(self.get('error_msg', error))
        sys.exit(self.getint('code', error))


