import os
import re
import sys
from gi.repository import Gtk

# Defining the current prog version
__version__ = "Version 1.0b1"
__python_version__ = "Python v" + ".".join (map (str, sys.version_info[:3]))
__gtk_version__ = "GTK v{}.{}.{}".format (Gtk.get_major_version(), Gtk.get_minor_version(), Gtk.get_micro_version())
__license__ = "GNU GPL version 2"


