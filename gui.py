#!/usr/bin/env python
__author__ = '4nto'

import logging
from concurrent import futures
import json

from gi.repository import Gtk
import requests

from util import NetworkInterfaces  # util.py
from socket import gethostname
import urllib2 

import subprocess, glib


logging.basicConfig(level=logging.DEBUG)
LOG = logging.getLogger(__name__)


class GUI(object):
    def __init__(self):
        global builder
        builder = Gtk.Builder()
        builder.add_from_file("gui.glade")
        builder.connect_signals(self)    

        # init network interfaces related fields
        self.ni = NetworkInterfaces()
        map(builder.get_object("combobox_ifs").append_text, self.ni.get_interfaces())
        builder.get_object("combobox_ifs").set_active(1)
        builder.get_object("label2").set_text("Randomize Hostname (now {})".format(gethostname()))  

#        html = urllib2.urlopen('https://check.torproject.org/?lang=en_US').read()
#        print html
#        tor_label = "Using Tor (currently " + ("UP"  if "Congratulations. This browser is configured to use Tor" in html else "DOWN") + ")"
#        builder.get_object("label4").set_text(tor_label)

    def write_to_buffer(self, fd, condition):
        if condition == glib.IO_IN:     #if there's something interesting to read
           char = fd.read(1)            # we read one byte per time, to avoid blocking
           buf = builder.get_object("textview1").get_buffer()
           buf.insert_at_cursor(char)   # When running don't touch the TextView!!
           return True                  # FUNDAMENTAL, otherwise the callback isn't recalled
        
        return False # Raised an error: exit and I don't want to see you anymore        

    def run(self, *args):
        builder.get_object("window").show()
        Gtk.main()

    def on_window_delete_event(self, *args):
        Gtk.main_quit(*args)

    def on_switch_pressed(self, switch, gparam):           
        map (lambda c: c.set_sensitive(switch.get_active()), builder.get_object("grid1").get_children())  
        builder.get_object("combobox_ifs").set_sensitive(switch.get_active()) 

        #proc = subprocess.Popen(['/bin/sh', '-c', './test.sh'], stdout = subprocess.PIPE) 
        proc = subprocess.Popen(['gksudo', 'sh', './anonymous', 'status'], stdout = subprocess.PIPE) 
        glib.io_add_watch(proc.stdout, glib.IO_IN,  self.write_to_buffer)           
        #MyTask().execute()

    def on_combobox_ifs_changed(self, combobox):
        ifname_active = builder.get_object("combobox_ifs").get_active_text()
        builder.get_object("label1").set_text("Randomize {} address (now {})".format(ifname_active, self.ni.get_addr(ifname_active)))

    def on_label_click(self, checkbutton, gparam):
        checkbutton.set_active(False if checkbutton.get_active() else True)
        

if __name__ == '__main__':
    GUI().run()
