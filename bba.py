#!/usr/bin/env python
__author__ = 'Antonio De Rosa'

from gi.repository import Gtk, GObject#, Gdk

from gui import GUI
from hostname import Hostname
from network import NetworkInterfaces
from tor import Tor
from bleachbit import Bleachbit
from util import __version__, __python_version__, __gtk_version__, __license__


class BBA(GUI):
    def __init__ (self, glade_file, log_file, css_file):
        GUI.__init__ (self, glade_file, log_file, css_file)

        self.combobox = self.get_object("cmb_mac")
        self.textview = self.get_object("textview1")
        
        toggleImg = lambda value: Gtk.STOCK_APPLY if value else Gtk.STOCK_CANCEL
        grouping = lambda items: items if type (items) is list else [items]

        self.setImg = lambda img, val: img.set_from_stock(toggleImg(val), Gtk.IconSize.BUTTON)
        self.write_in_textview = lambda text: self.textview.get_buffer().insert(self.textview.get_buffer().get_end_iter(), text)      
        self.prop2group = lambda g, p, v: map (lambda i: getattr (i, p)(v), filter (lambda i: hasattr (i, p), grouping(g)))
        
            
        self.ni =       NetworkInterfaces (self.log, self.write_in_textview)
        self.hname =    Hostname (self.log, self.write_in_textview)
        self.bleach =   Bleachbit (self.log, self.write_in_textview)
        self.tor =      Tor (self.log, self.write_in_textview)

        self.OnCheckEvents = {
            'network': {
                'check':    self.ni.check,
                'image':    self.get_object('img_mac'),
                'control':  self.get_object ('switch_mac'),
                'messages': ["You real address?", "Spoofed imp"]
                },
            self.get_object ('menu_hostname'): {
                'check':    self.hname.check,
                'image':    self.get_object('img_host'),
                'control':  self.get_object ('switch_host'),
                'messages': ["I know your name", "Fucking liar"]
                },
            self.get_object ('menu_clean'): {
                'check':    self.bleach.check,
                'image':    self.get_object('img_clean'),
                'control':  self.get_object ('button_clean'),
                'messages': ["Sad data in your pc..", "Cleaned shit"]
                },
            self.get_object ('menu_tor'): {
                'check':    self.tor.check,
                'image':    self.get_object('img_tor'),
                'control':  self.get_object ('switch_tor'),
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
        map (self.background_check, filter (lambda i: i != 'network', self.OnCheckEvents.keys()))
        
        #self.textview.override_background_color(Gtk.StateFlags.NORMAL,Gdk.RGBA(1.0,0.0,0.0,1))

    def background_check (self, control):
        d = self.OnCheckEvents[control]
        def background_check_callback(is_already):
            self.setImg (d['image'], is_already)
            self.prop2group (d['control'], 'set_active', is_already)
            self.prop2group (d['control'], 'set_sensitive', True)
            self.write_in_textview (d['messages'][1 if is_already else 0] + '\n')
            
        self.prop2group (d['control'], 'set_sensitive', False)
        d['check'](background_check_callback)            

    def on_cmb_mac_changed (self, *args):
        text = self.combobox.get_active_text() 
        selected_interface = text if text is None or '(default)' not in text else text[:-10]
        if selected_interface is not None:
            self.ni.select (selected_interface)
            
        self.background_check ('network')

    def on_menu_network_activate (self, *args):        
        self.ni.update()
        self.combobox.remove_all()
        if self.ni.get_default() is not None:
            self.combobox.append_text(self.ni.get_default() + " (default)")
        map (self.combobox.append_text, filter (lambda iface: iface != self.ni.get_default(), self.ni.get_interfaces()))        
        self.combobox.set_active(0) # it launches event CHANGED on combobox

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

    def on_menu_about_activate (self, *args):
        dialog = Gtk.MessageDialog (self.get_object("window"),
                                    0,
                                    Gtk.MessageType.INFO,
                                    Gtk.ButtonsType.OK,
                                    "BackBox Anonymizer")

        text = [__version__, __python_version__, __gtk_version__, '', __license__]        
        dialog.format_secondary_text ("\n".join (text))
        
        dialog.run()
        dialog.destroy()

    def on_menu_file_save_activate (self, *args):
        dialog =  Gtk.FileChooserDialog ("Please choose a file",
                                         self.get_object("window"),
                                         Gtk.FileChooserAction.SAVE,
                                         (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, "Select", Gtk.ResponseType.OK))

        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            with open(dialog.get_filename(), 'w') as f:
                f.write(self.textview.get_buffer().get_text(self.textview.get_buffer().get_start_iter(),
                                                            self.textview.get_buffer().get_end_iter(),
                                                            True))

            self.log.warning("Saved application log into {}".format(dialog.get_filename()))

        dialog.destroy()        

    def on_menu_clear_activate (self, *args):
        self.textview.get_buffer().delete(self.textview.get_buffer().get_start_iter(), self.textview.get_buffer().get_end_iter())


if __name__ == '__main__':
    bba = BBA("gui4.glade", "bba.log", "style.css")
    bba()        
