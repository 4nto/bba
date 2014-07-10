#!/usr/bin/env python
__author__ = '4nto'

import logging
from concurrent import futures
import json

from gi.repository import Gtk
import requests

from util import NetworkInterfaces  # util.py
from socket import gethostname


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

        # init terminal
        # terminal = Vte.Terminal()
        # terminal.connect('realize', self.on_realize_terminal)
        # builder.get_object("scrolledwindow1").add(terminal)

        #self.tb = builder.get_object("textview1").get_buffer()        

    def run(self, *args):
        builder.get_object("window").show()
        Gtk.main()

    def on_window_delete_event(self, *args):
        Gtk.main_quit(*args)

    def on_switch_pressed(self, switch, gparam):           
        map (lambda c: c.set_sensitive(switch.get_active()), builder.get_object("grid1").get_children())  
        builder.get_object("combobox_ifs").set_sensitive(switch.get_active()) 

        builder.get_object("textview1").get_buffer().insert(builder.get_object("textview1").get_buffer().get_end_iter(), "ENABLED\n" if switch.get_active() else "DISABLED\n")       
        #MyTask().execute()

    def on_combobox_ifs_changed(self, combobox):
        ifname_active = builder.get_object("combobox_ifs").get_active_text()
        builder.get_object("label1").set_text("Randomize {} address (now {})".format(ifname_active, self.ni.get_addr(ifname_active)))

    def on_label_click(self, checkbutton, gparam):
        checkbutton.set_active(False if checkbutton.get_active() else True)
        

if __name__ == '__main__':
    GUI().run()
