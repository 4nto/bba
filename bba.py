#!/usr/bin/env python
__author__ = 'Antonio De Rosa'

from gi.repository import Gtk, GObject

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

        self.OnCheckEvents = {
            self.get_object ('menu_network'): {
                'check':    self.ni.check,
                'image':    'img_mac',
                'control':  'switch_mac',
                'messages': ["You real address?", "Spoofed imp"]
                },
            self.get_object ('menu_hostname'): {
                'check': self.hname.check,
                'image': 'img_host',
                'control': 'switch_host',
                'messages': ["I know your name", "Fucking liar"]
                },
            self.get_object ('menu_clean'): {
                'check': self.bleach.check,
                'image': 'img_clean',
                'control': 'button_clean',
                'messages': ["Sad data in your pc..", "Cleaned shit"]
                },
            self.get_object ('menu_tor'): {
                'check': self.tor.check,
                'image': 'img_tor',
                'control': 'switch_tor',
                'messages': ["You're visible", "Anonymous bastard"]
                }
            }

        self.OnGoEvents = {
            self.get_object ('switch_mac'): {
                'active':   self.ni.reset,
                'inactive': self.ni.set,
                'callback': self.on_cmb_mac_changed
                },
            self.get_object ('switch_host'): {
                'active':   self.hname.reset,
                'inactive': self.hname.randomize,
                'callback': lambda: self.background_check (self.get_object ('menu_hostname'))
                },
            self.get_object ('button_clean'): {
                'active':   self.bleach.start,
                'callback': lambda: self.background_check (self.get_object ('menu_clean'))
                },
            self.get_object ('switch_tor'): {
                'active':   self.tor.stop,
                'inactive': self.tor.start,
                'callback': lambda: self.background_check (self.get_object ('menu_tor'))
                }
            }
        
        self.on_menu_network_activate()
        map (self.background_check, (self.get_object ('menu_hostname'), self.get_object ('menu_clean'), self.get_object ('menu_tor')))
        '''
        self.on_menu_network_activate()        
        self.on_menu_hostname_activate()
        self.on_menu_clean_activate()
        self.on_menu_tor_activate()
        '''
        #self.sensitive (['switch_host', 'switch_mac', 'button_clean', 'switch_tor'], False)
    '''            
    def on_menu_hostname_activate (self, *args):
        self.background_check(self.hname.check, "img_host", "switch_host", ["I know your name", "Fucking liar"])

    def on_menu_clean_activate (self, *args):
        self.background_check(self.bleach.check, "img_clean", "button_clean", ["Sad data in your pc..", "Cleaned shit"])

    def on_menu_tor_activate (self, *args):
        self.background_check(self.tor.check, "img_tor", "switch_tor", ["You're visible", "Anonymous bastard"])
    '''        
    '''
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
    '''
    def background_check (self, control):
        d = self.OnCheckEvents[control]
        def background_check_callback(is_already):
            self.setImg (d['image'], is_already)
            if hasattr (self.get_object (d['control']), "set_active"):
                self.get_object (d['control']).set_active (is_already)
            self.get_object(d['control']).set_sensitive (True)
            self.sensitive ([d['control']], True)
            self.write_in_textview (d['messages'][1 if is_already else 0] + '\n')
            
        self.sensitive ([d['control']], False)
        d['check'](background_check_callback)            

    def on_cmb_mac_changed (self, *args):
        text = self.get_object("cmb_mac").get_active_text() 
        selected_interface = text if text is None or '(default)' not in text else text[:-10]
        if selected_interface is not None:
            self.ni.select (selected_interface)
        self.background_check (self.get_object ('menu_network'))
        #self.background_check(self.ni.check, "img_mac", "switch_mac", ["You real address?", "Spoofed imp"])

    def on_menu_network_activate (self, *args):
        combobox = self.get_object("cmb_mac")
        self.ni.update()
        combobox.remove_all()
        if self.ni.get_default() is not None:
            combobox.append_text(self.ni.get_default() + " (default)")
        map (combobox.append_text, filter (lambda iface: iface != self.ni.get_default(), self.ni.get_interfaces()))        
        combobox.set_active(0)
        self.on_cmb_mac_changed()

    def on_press_event (self, control, *args):
        control.set_sensitive(False)
        if hasattr(control, "set_active") and not control.get_active():
            self.OnGoEvents[control]['inactive'] (self.OnGoEvents[control]['callback'])
        else:
            self.OnGoEvents[control]['active'] (self.OnGoEvents[control]['callback'])

    #autoscroll
    def on_textview_sizeallocate_event (self, textview, *args):
        adj = textview.get_vadjustment()
        adj.set_value(adj.get_upper() - adj.get_page_size())        

if __name__ == '__main__':
    bba = BBA("gui4.glade", "bba.log")
    bba()        
