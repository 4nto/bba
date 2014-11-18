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
        self.__init_dialogs()
        self.get_object("window").show()
        Gtk.main()

    def __init_dialogs(self):
        dialog = self.get_object("aboutdialog")
        try:
            with open('doc/LICENSE') as lfile:
                dialog.set_license(lfile.read().replace('\x0c', ''))
        except IOError:
            dialog.set_license("License file is missing")        

        dialog = self.get_object("infodialog")
        python = '.'.join(map(str, sys.version_info[:3]))
        gtk = '{}.{}.{}'.format(Gtk.get_major_version(),
                                Gtk.get_minor_version(),
                                Gtk.get_micro_version())
        
        text = "You are using <b>Python v{}</b> and <b>GTK v{}</b>".format(python, gtk)
        dialog.set_markup(text)

    def on_window_delete_event(self, *args):
        Gtk.main_quit(*args)
        
    def on_menu_activate(self, dialog):
        '''Show menu form'''            
        dialog.run()
        dialog.hide()
      

        
