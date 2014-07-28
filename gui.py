#!/usr/bin/env python
__author__ = '4nto'

import logging
from concurrent import futures
import json

from gi.repository import Gtk
import requests

from hostname import Hostname
from networkinterfaces import NetworkInterfaces
from tor import Tor
import urllib2 

import subprocess, glib, shlex

import time, os #toremove


logging.basicConfig(level=logging.DEBUG)
LOG = logging.getLogger(__name__)


class GUI(object):
    def __init__(self):
        global builder
        builder = Gtk.Builder()
        builder.add_from_file("gui3.glade")
        builder.connect_signals(self)

        builder.get_object("image6").set_from_stock(Gtk.STOCK_CLEAR, Gtk.IconSize.BUTTON)
        
        self.testcmd = Tor(LOG, self.write_to_buffer)
        self.tor = Tor(LOG, self.write_to_buffer)
        self.hname = Hostname(LOG)
        self.ni = NetworkInterfaces(LOG, self.write_to_buffer)

        self.wconsole_c = lambda text: builder.get_object("textview1").get_buffer().insert_at_cursor(text)
        self.wconsole = lambda text: self.wconsole_c (text + '\n')
        self.setImg = lambda image, value: image.set_from_stock(Gtk.STOCK_APPLY if value else Gtk.STOCK_CANCEL, Gtk.IconSize.BUTTON)
        self.update_netiface_info(builder.get_object("combobox_ifs"))            
        #self.filter_default = lambda text: self.ni.get_default() if "(default)" in text else text       
        
        self.is_root = os.geteuid() == 0
        if not self.is_root:
            self.wconsole("You are not root!")
            map (lambda c: c.set_sensitive(True), builder.get_object("grid1").get_children())

    def toggle_sensitive(self, obj):
        obj.set_sensitive(not obj.get_sensitive())

    def update_netiface_info(self, combobox):
        self.ni.update()
        combobox.remove_all()
        combobox.append_text(self.ni.get_default() + " (default)")
        map (combobox.append_text, filter (lambda iface: iface != self.ni.get_default(), self.ni.get_interfaces()))        
        combobox.set_active(0)        

    def write_to_buffer(self, fd, condition):
        if condition == glib.IO_IN:     #if there's something interesting to read
           char = fd.read(1)            # we read one byte per time, to avoid blocking
           self.wconsole_c(char)
           return True                  # FUNDAMENTAL, otherwise the callback isn't recalled
        
        return False # Raised an error: exit and I don't want to see you anymore        

    def on_switch_pressed(self, switch, gparam):           
        #map (lambda c: c.set_sensitive(switch.get_active()), builder.get_object("box").get_children()) 
        self.toggle_sensitive(switch) 
        self.testcmd.set_callback(lambda a, b: self.toggle_sensitive(switch))
        self.testcmd.run()    

    def on_combobox_ifs_changed(self, combobox):
        if combobox.get_active_text() is None:
            return

        filter_default = lambda text: self.ni.get_default() if "(default)" in text else text
        ifname = filter_default (combobox.get_active_text())

        self.wconsole("{} current MAC address is {} ".format(ifname, "the real-one" if self.ni.is_spoofed(ifname) else "already spoofed!"))
        self.setImg(builder.get_object("img_mac"), not self.ni.is_spoofed(ifname))

    def toggle_show_tor(self, togglecontent):        
        results = ("", Gtk.STOCK_APPLY) if self.tor.check() else ("not ", Gtk.STOCK_CANCEL)
        togglecontent.set_from_stock(results[1], Gtk.IconSize.BUTTON)
        self.wconsole("You are " + results[0] + "using Tor!")

    def update_hostname_info(self, button):
        if not self.hname.check():
            self.wconsole("The current hostname ({}) is already spoofed from the last boot!".format(self.hname.get()))
            button.set_active(True)

    def on_button_mac_clicked (self, button):
        filter_default = lambda text: self.ni.get_default() if "(default)" in text else text
        ifname = filter_default(builder.get_object("combobox_ifs").get_active_text())
        self.toggle_sensitive(button)        
        self.ni.set (ifname, lambda a,b: self.update_img_mac(button, ifname))

    def update_img_mac (self, button, ifname):
        print "GOING TO CHECK " + ifname + " ADDR"
        builder.get_object("img_mac").set_from_stock(Gtk.STOCK_APPLY if not self.ni.check(ifname) else Gtk.STOCK_CANCEL, Gtk.IconSize.BUTTON)
        self.toggle_sensitive(button)

    def run(self, *args):
        builder.get_object("window").show()
        Gtk.main()

    def on_window_delete_event(self, *args):
        Gtk.main_quit(*args)

if __name__ == '__main__':
    GUI().run()
