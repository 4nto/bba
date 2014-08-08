#!/usr/bin/env python
# Thanks to jdi from stackoverflow.com/questions/11191398
__author__ = 'Antonio De Rosa'

from gui import GUI
from gi.repository import Gtk

from hostname import Hostname
from networkinterfaces import NetworkInterfaces
from tor import Tor
from bleachbit import Bleachbit

class BBA(GUI):
    def __init__ (self, glade_file, log_file):
    	GUI.__init__ (self, glade_file, log_file)

    	self.wconsole = lambda text: self.get_object("textview1").get_buffer().insert_at_cursor(text + '\n')
        self.toggleImg = lambda value: Gtk.STOCK_APPLY if value else Gtk.STOCK_CANCEL
        self.setImg = lambda img, val: self.get_object(img).set_from_stock(self.toggleImg(val), Gtk.IconSize.BUTTON)    

    	self.ni = NetworkInterfaces(self.warning, self.get_object("textview1").get_buffer().insert_at_cursor)
        self.hname = Hostname(self.warning, self.get_object("textview1").get_buffer().insert_at_cursor)
        self.bleach = Bleachbit(self.warning, self.get_object("textview1").get_buffer().insert_at_cursor)
        self.tor = Tor(self.warning, self.get_object("textview1").get_buffer().insert_at_cursor)

    	self.on_menu_network_activate(self.get_object("cmb_mac"))
        self.on_menu_hostname_activate()
        self.on_menu_clean_activate()
        self.on_menu_tor_activate()

    def background_check (self, check, image, button, message):
        def background_check_callback(is_already):
            self.setImg (image, is_already)
            if hasattr(self.get_object(button), "set_active"):
            	self.get_object(button).set_active(is_already)
            self.get_object(button).set_sensitive(True)
            self.wconsole (message[1 if is_already else 0])

        self.get_object(button).set_sensitive(False)
        check(background_check_callback)

    def on_menu_hostname_activate (self, *args):
    	result = self.hname.check()
        self.setImg ("img_host", result)
        self.get_object("switch_host").set_active(result)
        self.get_object("switch_host").set_sensitive(True)

    def on_menu_clean_activate (self, *args):
        self.background_check(self.bleach.check, "img_clean", "button_clean", ["Sad data in your pc..", "Cleaned bastard"])

    def on_menu_tor_activate (self, *args):
        self.background_check(self.tor.check, "img_tor", "switch_tor", ["You're visible, idiot..", "Anonymous bastard"])

    def on_menu_network_activate (self, combobox):
        self.ni.update()
        combobox.remove_all()
        combobox.append_text(self.ni.get_default() + " (default)")
        map (combobox.append_text, filter (lambda iface: iface != self.ni.get_default(), self.ni.get_interfaces()))        
        combobox.set_active(0) 
        self.on_cmb_mac_changed (combobox)

    def on_cmb_mac_changed (self, combobox):
        self.setImg ("img_mac", self.ni.check(self.selected_interface()))

    def on_button_mac_clicked (self, button):
        def on_button_mac_clicked_callback (*args):            
            self.setImg ('img_mac', self.ni.check(self.selected_interface()))
            button.set_sensitive(True)

        button.set_sensitive(False)
        self.ni.set_callback (on_button_mac_clicked_callback)
        self.ni.set (self.selected_interface())        

    def selected_interface(self):
        text = self.get_object("cmb_mac").get_active_text()
        return self.ni.get_default() if text is None or '(default)' in text else text 

    def on_switch_host_button_release_event (self, switch, *args):
        switch.set_sensitive(False) 
        self.hname.set_callback (self.on_menu_hostname_activate)
        if switch.get_active():	self.hname.reset()               
        else:					self.hname.set (self.hname.random())


    def on_button_clean_clicked (self, button):
    	button.set_sensitive(False)
    	self.bleach.set_callback (self.on_menu_clean_activate)
    	self.bleach.start()

    def on_switch_tor_button_release_event (self, switch, *args):
    	switch.set_sensitive(False)
    	self.tor.set_callback (self.on_menu_tor_activate)
    	if switch.get_active():	self.tor.stop()    		
    	else:					self.tor.start()


if __name__ == '__main__':
    bba = BBA("gui4.glade", "bba.log")
    bba()        
