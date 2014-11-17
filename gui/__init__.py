import logging
import sys
import os
from gi.repository import Gtk, Gdk

class GUI(Gtk.Builder):
    def __init__(self, glade_file, log_file, css_file):
        super(GUI, self).__init__()
        self.add_from_file(glade_file)
        self.connect_signals(self)

        css = Gtk.CssProvider()
        with open(css_file) as fd:
            css.load_from_data(fd.read())
        #css.load_from_file(css_data) doesn't work
        
        Gtk.StyleContext.add_provider_for_screen(Gdk.Screen.get_default(),\
                    css, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
        
        self.log = logging.getLogger(__name__)
        fh = logging.FileHandler(log_file)
        fh.setLevel(logging.DEBUG)				
        ch = logging.StreamHandler()
        ch.setLevel(logging.ERROR)
        formatter = logging.Formatter\
                    ('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        fh.setFormatter(formatter)
        ch.setFormatter(formatter)
        self.log.addHandler(fh)
        self.log.addHandler(ch)

    def __call__(self):
        self.get_object("window").show()
        Gtk.main()

    def on_window_delete_event(self, *args):
        Gtk.main_quit(*args)
        
    def on_menu_about_activate(self, dialog):
        '''Show About form'''
        try:
            with open('doc/LICENSE') as lfile:
                dialog.set_license(lfile.read().replace('\x0c', ''))
        except IOError:
            dialog.set_license("License file is missing")
            
        dialog.run()
        dialog.hide()

    def on_menu_info_activate(self, dialog):
        '''Show Info form'''
        dialog.set_markup("Python v" + ".".join (map (str, sys.version_info[:3])))
        dialog.format_secondary_markup("GTK v{}.{}.{}".format (Gtk.get_major_version(), Gtk.get_minor_version(), Gtk.get_micro_version()))
        dialog.run()
        dialog.hide()        

        
