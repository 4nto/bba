#!/usr/bin/env python
__author__ = 'Antonio De Rosa'

from gi.repository import Gtk

from gui import GUI
from hostname import Hostname
from network import NetworkInterfaces
from tor import Tor
from bleachbit import Bleachbit

class BBA(GUI):
    def __init__ (self, glade_file, log_file):
        GUI.__init__ (self, glade_file, log_file)

        self.toggleImg = lambda value: Gtk.STOCK_APPLY if value else Gtk.STOCK_CANCEL
        self.setImg = lambda img, val: self.get_object(img).set_from_stock(self.toggleImg(val), Gtk.IconSize.BUTTON)
        self.write_in_textview = lambda text: self.get_object("textview1").get_buffer().insert_at_cursor(text)
        self.sensitive = lambda group, value: map (lambda item: self.get_object(item).set_sensitive(value), group)
            
        self.ni =       NetworkInterfaces (self.log, self.write_in_textview)
        self.hname =    Hostname (self.log, self.write_in_textview)
        self.bleach =   Bleachbit (self.log, self.write_in_textview)
        self.tor =      Tor (self.log, self.write_in_textview)

        self.on_menu_network_activate(self.get_object("cmb_mac"))
        self.on_menu_hostname_activate()
        self.on_menu_clean_activate()
        self.on_menu_tor_activate()
        #self.sensitive (['switch_host', 'button_mac', 'button_clean', 'switch_tor'], False)

    def background_check (self, check, image, button, message):
        def background_check_callback(is_already):
            self.setImg (image, is_already)
            if hasattr(self.get_object(button), "set_active"):
                self.get_object(button).set_active(is_already)
            self.get_object(button).set_sensitive(True)
            self.sensitive ([button], True)
            self.write_in_textview (message[1 if is_already else 0] + '\n')

        self.sensitive ([button], False)
        check(background_check_callback)

    def on_menu_hostname_activate (self, *args):
        self.background_check(self.hname.check, "img_host", "switch_host", ["I know your name", "Fucking liar"])

    def on_menu_clean_activate (self, *args):
        self.background_check(self.bleach.check, "img_clean", "button_clean", ["Sad data in your pc..", "Cleaned shit"])

    def on_menu_tor_activate (self, *args):
        self.background_check(self.tor.check, "img_tor", "switch_tor", ["You're visible", "Anonymous bastard"])

    def on_cmb_mac_changed (self, *args):
        self.ni.select (self.selected_interface())
        self.background_check(self.ni.check, "img_mac", "button_mac", ["You real address?", "Spoofed imp"])

    def on_menu_network_activate (self, combobox):
        self.ni.update()
        combobox.remove_all()
        combobox.append_text(self.ni.get_default() + " (default)")
        map (combobox.append_text, filter (lambda iface: iface != self.ni.get_default(), self.ni.get_interfaces()))        
        combobox.set_active(0) 
        self.on_cmb_mac_changed()

    def selected_interface(self):
        text = self.get_object("cmb_mac").get_active_text()
        return self.ni.get_default() if text is None or '(default)' in text else text

    def on_button_mac_clicked (self, button):
        button.set_sensitive(False)
        self.ni.set (self.selected_interface(), self.on_cmb_mac_changed)         

    def on_switch_host_button_press_event (self, switch, *args):
        switch.set_sensitive(False)         
        if switch.get_active():
            self.hname.reset (self.on_menu_hostname_activate)
        else:
            self.hname.randomize (self.on_menu_hostname_activate)

    def on_button_clean_clicked (self, button):
        button.set_sensitive(False)
        self.bleach.start(self.on_menu_clean_activate)

    def on_switch_tor_button_press_event (self, switch, *args):               
        switch.set_sensitive(False)
        if switch.get_active():
            self.tor.stop (self.on_menu_tor_activate)         
        else:
            self.tor.start(self.on_menu_tor_activate)


if __name__ == '__main__':
    bba = BBA("gui4.glade", "bba.log")
    bba()        
