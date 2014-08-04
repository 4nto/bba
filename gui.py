#!/usr/bin/env python
# Thanks to jdi from stackoverflow.com/questions/11191398
__author__ = '4nto'

import logging
from gi.repository import Gtk

from hostname import Hostname
from networkinterfaces import NetworkInterfaces
from tor import Tor
from bleachbit import Bleachbit

from threading import Thread
import glib

class GUI(Gtk.Builder, logging.Logger):
    def __init__(self, glade_file, log_file):
    	def init_gtk():
        	Gtk.Builder.__init__(self)
        	self.add_from_file(glade_file)
        	self.connect_signals(self)	

    	def init_logging():
        	logging.Logger.__init__(self, __name__)
        	fh = logging.FileHandler(log_file)
        	fh.setLevel(logging.DEBUG)				
        	ch = logging.StreamHandler()
        	ch.setLevel(logging.ERROR)
        	formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        	fh.setFormatter(formatter)
        	ch.setFormatter(formatter)
        	self.addHandler(fh)
        	self.addHandler(ch)

        init_gtk()
        init_logging()

    	'''Internal stuff'''
    	self.wconsole = lambda text: self.get_object("textview1").get_buffer().insert_at_cursor(text + '\n')
        self.toggleImg = lambda value: Gtk.STOCK_APPLY if value else Gtk.STOCK_CANCEL
        self.setImg = lambda img, val: self.get_object(img).set_from_stock(self.toggleImg(val), Gtk.IconSize.BUTTON)    

    	self.ni = NetworkInterfaces(self.warning, self.get_object("textview1").get_buffer().insert_at_cursor)
        self.hname = Hostname(self.warning, self.get_object("textview1").get_buffer().insert_at_cursor)
        self.bleach = Bleachbit(self.warning, self.get_object("textview1").get_buffer().insert_at_cursor)
        self.tor = Tor(self.warning, self.get_object("textview1").get_buffer().insert_at_cursor)

    	self.update_netiface_info(self.get_object("cmb_mac"))
        self.setImg ("img_mac", self.ni.check())
        self.setImg ("img_host", self.hname.check())      

        self.background_check(self.bleach.check, "img_clean", "button_clean", ["Sad data in your pc..", "Cleaned bastard"])
        self.background_check(self.tor.check, "img_tor", "switch_set", ["You're visible, idiot..", "Anonymous bastard"])

    def background_check (self, check, image, button, message):
        def background_check_callback(is_already):
            self.setImg (image, is_already)
            self.get_object(button).set_sensitive(True)
            self.wconsole (message[1 if is_already else 0])

        self.get_object(button).set_sensitive(False)
        check(background_check_callback)

        #Thread (target = bleach_check, args = ["img_clean", "button_clean"]).start()

    def update_netiface_info(self, combobox):
        self.ni.update()
        combobox.remove_all()
        combobox.append_text(self.ni.get_default() + " (default)")
        map (combobox.append_text, filter (lambda iface: iface != self.ni.get_default(), self.ni.get_interfaces()))        
        combobox.set_active(0) 

    def __call__(self):
        self.get_object("window").show()
        Gtk.main()

    def on_window_delete_event(self, *args):
        Gtk.main_quit(*args)

    def on_button_mac_clicked(self, button):
        def on_button_mac_clicked_callback(dum1, dum2):            
            self.setImg ('img_mac', self.ni.check(self.selected_interface()))
            button.set_sensitive(True)

        button.set_sensitive(False)
        self.ni.set_callback (on_button_mac_clicked_callback)
        self.ni.set (self.selected_interface())        

    def selected_interface(self):
        text = self.get_object("cmb_mac").get_active_text()
        return self.ni.get_default() if '(default)' in text else text 

    def on_button_host_clicked(self, button):
        def on_button_host_clicked_callback(dum1, dum2):            
            self.setImg ("img_host", self.hname.check())
            button.set_sensitive(True)

        button.set_sensitive(False) 
        self.hname.set_callback (on_button_host_clicked_callback)
        #self.hname.set (self.hname.random())
        self.hname.reset()

if __name__ == '__main__':
    bba = GUI("gui4.glade", "bba.log")
    bba()
