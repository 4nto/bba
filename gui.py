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
        builder.add_from_file("gui2.glade")
        builder.connect_signals(self)

        self.ni = NetworkInterfaces()
        self.wconsole = lambda text: builder.get_object("textview1").get_buffer().insert_at_cursor(text + '\n')
        self.update_netiface_info(builder.get_object("combobox_ifs"))           
        #self.label_append (builder.get_object("lbl_hostname"), "\"{}\"".format(gethostname()))
        

    def update_netiface_info(self, combobox):
        self.ni.update()
        combobox.remove_all()
        combobox.append_text(self.ni.get_default() + " (default)")
        map (combobox.append_text, filter (lambda iface: iface != self.ni.get_default(), self.ni.get_interfaces()))        
        combobox.set_active(0)        

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
        map (lambda c: c.set_sensitive(switch.get_active()), builder.get_object("box").get_children())  
        proc = subprocess.Popen(['gksudo', 'sh', './anonymous', 'status'], stdout = subprocess.PIPE) 
        glib.io_add_watch(proc.stdout, glib.IO_IN,  self.write_to_buffer)           
        #MyTask().execute()

    def on_combobox_ifs_changed(self, combobox):
        if combobox.get_active_text() is None:
            return

        ifname = self.ni.get_default() if "(default)" in combobox.get_active_text() else combobox.get_active_text()
        #builder.get_object("lbl_mac").set_text("Your current MAC address " + ("is the real-one" if self.ni.is_spoofed(ifname) else "is already spoofed!"))        
        #builder.get_object("lbl_mac").set_visible(not self.ni.is_spoofed(ifname))
        self.wconsole("{} current MAC address is {} ".format(ifname, "the real-one" if self.ni.is_spoofed(ifname) else "already spoofed!"))
        builder.get_object("checkbutton1").set_active(not self.ni.is_spoofed(ifname))

    def toggle_show(self, togglecontent):
        togglecontent.set_visible(not togglecontent.get_visible())

    def toggle_show_tor(self, togglecontent):
        #if not togglecontent.get_visible():
        self.wconsole("You " + ("are"  if self.check_tor() else "are not") + " using Tor") 

        #self.toggle_show(togglecontent)    

    def check_tor(self):
        html = urllib2.urlopen('https://check.torproject.org/?lang=en_US').read()
        return True  if "Congratulations. This browser is" in html else False

    def update_hostname_info(self, button):
        if not self.check_hostname():
            self.wconsole("The current hostname ({}) is already spoofed from the last boot!".format(gethostname()))
            button.set_active(True)

    def check_hostname(self):      
        proc = subprocess.Popen(['fgrep', 'Linux version', '/var/log/kern.log'], stdout=subprocess.PIPE)
        try:
            hostname_original = proc.stdout.readline()[:-1].split()[3]
        except:
            LOG.debug("Unable to open kern.log or parsing it")
            return True

        return gethostname() == hostname_original

if __name__ == '__main__':
    GUI().run()
