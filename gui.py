import logging
import os
from gi.repository import Gtk, Gdk

class GUI(Gtk.Builder):
    def __init__(self, glade_file, log_file, css_file):
        Gtk.Builder.__init__(self)
        self.add_from_file(glade_file)
        self.connect_signals(self)

        css = Gtk.CssProvider()
        css.load_from_data('@import url("{}");'.format(css_file)) #css.load_from_file(css_file) doesn't work        
        
        Gtk.StyleContext.add_provider_for_screen(Gdk.Screen.get_default(),
                                                 css,
                                                 Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
        
        self.log = logging.getLogger(__name__)
        fh = logging.FileHandler(log_file)
        fh.setLevel(logging.DEBUG)				
        ch = logging.StreamHandler()
        ch.setLevel(logging.ERROR)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        fh.setFormatter(formatter)
        ch.setFormatter(formatter)
        self.log.addHandler(fh)
        self.log.addHandler(ch)

    def __call__(self):
        self.get_object("window").show()
        Gtk.main()

    def on_window_delete_event(self, *args):
        Gtk.main_quit(*args)

class WrappedFileChooserDialog(Gtk.FileChooserDialog):
    def __init__(self, *args):
        Gtk.FileChooserDialog.__init__(self, *args)
        self.set_current_folder(os.path.dirname(os.path.abspath(__file__)))
        
    def __enter__(self):
        return {'response': self.run(), 'dialog': self}
    
    def __exit__(self, *args):
        self.destroy()
