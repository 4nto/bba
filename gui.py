import logging
from gi.repository import Gtk

class GUI(Gtk.Builder):
    def __init__(self, glade_file, log_file):
        Gtk.Builder.__init__(self)
        self.add_from_file(glade_file)
        self.connect_signals(self)
        
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
