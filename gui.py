#!/usr/bin/env python
__author__ = 'leinardi'

import logging
from concurrent import futures
import json

from gi.repository import Gtk
import requests

from util import NetworkInterfaces  # util.py
from socket import gethostname


logging.basicConfig(level=logging.DEBUG)
LOG = logging.getLogger(__name__)


class Helloworld(object):
    def __init__(self):
        global builder
        builder = Gtk.Builder()
        builder.add_from_file("helloworld.glade")
        builder.connect_signals(self)    

        self.ni = NetworkInterfaces()

        map(builder.get_object("combobox_ifs").append_text, self.ni.get_interfaces())
        builder.get_object("combobox_ifs").set_active(1)

        builder.get_object("label2").set_text("Randomize Hostname (now {})".format(gethostname()))

    def run(self, *args):
        builder.get_object("window").show()
        Gtk.main()

    def on_window_delete_event(self, *args):
        Gtk.main_quit(*args)

    def on_switch_pressed(self, switch, gparam):           
        map (lambda c: c.set_sensitive(switch.get_active()), builder.get_object("grid1").get_children())  
        builder.get_object("combobox_ifs").set_sensitive(switch.get_active())        
        #MyTask().execute()

    def on_combobox_ifs_changed(self, combobox):
        ifname_active = builder.get_object("combobox_ifs").get_active_text()
        builder.get_object("label1").set_text("Randomize {} address (now {})".format(ifname_active, self.ni.get_addr(ifname_active)))

    def on_label_click(self, checkbutton, gparam):
        checkbutton.set_active(False if checkbutton.get_active() else True)
        

if __name__ == '__main__':
    Helloworld().run()
