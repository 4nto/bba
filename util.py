import os
import re
import sys
from gi.repository import Gtk, GObject

# Defining the current prog version
__version__ = "Version 0.9"
__python_version__ = "Python v" + ".".join (map (str, sys.version_info[:3]))
__gtk_version__ = "GTK v{}.{}.{}".format (Gtk.get_major_version(), Gtk.get_minor_version(), Gtk.get_micro_version())
__license__ = "GNU GPL version 2"

def command_exist(fpath):
    return os.path.isfile(fpath) and os.access(fpath, os.X_OK)

# Thanks to haridsv from stackoverflow.com/questions/1714027
def version_cmp(version1, version2):
    def normalize(v):
        return map (int, re.sub (r'(\.0+)*$','', v).split("."))
    return cmp (normalize(version1), normalize(version2))

# Thanks to ssokolow from http://stackoverflow.com/questions/2761829
def get_default_gateway_linux():
    with open("/proc/net/route") as fh:
        for line in fh:
            fields = line.strip().split()
            if fields[1] != '00000000' or not int(fields[3], 16) & 2:
                continue

            return fields[0]
