#!/usr/bin/env python
__author__ = '4nto'

import logging
from concurrent import futures
import json

from gi.repository import Gtk
import requests

from util import NetworkInterfaces, Hostname, Batch  # util.py
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
        
        self.testcmd = Batch("sh ./test.sh", self.write_to_buffer)

        self.hname = Hostname(LOG)
        self.ni = NetworkInterfaces(LOG)
        self.wconsole = lambda text: builder.get_object("textview1").get_buffer().insert_at_cursor(text + '\n')
        self.setImg = lambda image, value: image.set_from_stock(Gtk.STOCK_APPLY if value else Gtk.STOCK_CANCEL, Gtk.IconSize.BUTTON)
        self.update_netiface_info(builder.get_object("combobox_ifs"))           
        
        self.is_root = os.geteuid() == 0
        if not self.is_root:
            self.wconsole("You are not root!")
            map (lambda c: c.set_sensitive(True), builder.get_object("grid1").get_children())

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
        #map (lambda c: c.set_sensitive(switch.get_active()), builder.get_object("box").get_children())  
        self.testcmd.run()    
        #MyTask().execute()

    def on_combobox_ifs_changed(self, combobox):
        if combobox.get_active_text() is None:
            return

        ifname = self.ni.get_default() if "(default)" in combobox.get_active_text() else combobox.get_active_text()
        self.wconsole("{} current MAC address is {} ".format(ifname, "the real-one" if self.ni.is_spoofed(ifname) else "already spoofed!"))
        self.setImg(builder.get_object("img_mac"), not self.ni.is_spoofed(ifname))


    def toggle_show(self, togglecontent):
        self.execute(self.test_sleep(), self.test_feedback())

    def test_sleep(self):
        builder.get_object("button_mac").set_sensitive(False)
        #builder.get_object("image8").set_from_stock(Gtk.STOCK_EXECUTE, Gtk.IconSize.BUTTON)
        time.sleep(5)

    def test_feedback(self):
        builder.get_object("button_mac").set_sensitive(True)
        builder.get_object("image8").set_from_stock(Gtk.STOCK_APPLY, Gtk.IconSize.BUTTON)

    def toggle_show_tor(self, togglecontent):
        #if not togglecontent.get_visible():
        self.wconsole("You " + ("are"  if self.check_tor() else "are not") + " using Tor") 

        #self.toggle_show(togglecontent)    

    def check_tor(self):
        html = urllib2.urlopen('https://check.torproject.org/?lang=en_US').read()
        return True  if "Congratulations. This browser is" in html else False

    def update_hostname_info(self, button):
        if not self.check_hostname():
            self.wconsole("The current hostname ({}) is already spoofed from the last boot!".format(self.hname.get()))
            button.set_active(True)

    def execute(self, my_task, on_task_complete):
        # executor = futures.ProcessPoolExecutor(max_workers=1)
        executor = futures.ThreadPoolExecutor(max_workers=1)
        future = executor.submit(my_task)
        future.add_done_callback(on_task_complete)

def ExecuteCommand(cmd, writer):
    assert isinstance(cmd, str) and hasattr(writer, '__call__')
    proc = subprocess.Popen(shlex.split(cmd if os.geteuid() == 0 else "gksudo " + cmd), stdout = subprocess.PIPE)
    glib.io_add_watch(proc.stdout, glib.IO_IN, writer)

if __name__ == '__main__':
    GUI().run()
