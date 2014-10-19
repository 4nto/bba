import logging
import os
from gi.repository import Gtk, Gdk

class GUI(Gtk.Builder):
    def __init__(self, glade_file, log_file, css_file):
        Gtk.Builder.__init__(self)
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

class WrappedFileChooserDialog(Gtk.FileChooserDialog):
    def __init__(self, *args):
        Gtk.FileChooserDialog.__init__(self, *args)
        self.set_current_folder(os.path.dirname(os.path.abspath(__file__)))
        
    def __enter__(self):
        return {'response': self.run(), 'dialog': self}
    
    def __exit__(self, *args):
        self.destroy()

class PanedSwitchLabel(Gtk.Paned):
    def __init__(self, wrapper):
        '''Create the combination switch/label or button/label in the paned'''
        Gtk.Paned.__init__(self)
        self.wrapper = wrapper
        
        self.set_position(100)
        self.label = Gtk.Label(wrapper.config.get('config', 'title'))
        self.label.set_halign(Gtk.Align.START)
        self.label.set_sensitive(False)
        self.switch = Gtk.Switch()
        self.switch.set_margin_left(10)
        self.switch.set_margin_right(20)
        self.switch.set_valign(Gtk.Align.CENTER)
        self.switch.set_active(False)
        self.switch.set_sensitive(False)
        self.add1(self.switch)
        self.add2(self.label)
        self.show_all()

    def connect_wrapper(self):
        '''Connect widget signals to the functions managed by the wrapper'''
        def check_callback(is_already):
            self.switch.set_active(is_already)
            self.switch.set_sensitive(True)
        
        def callback(*args):            
            self.wrapper.check(check_callback)
                
        def toggle(widget, *args):
            widget.set_sensitive(False)
            if widget.get_active():
                self.wrapper.stop(callback)
            else:
                self.wrapper.start(callback)
                                           
        self.switch.connect('button-press-event', toggle)        

    def enable_widget(self):
        '''Enable the widget if the step VERIFY returns with no errors'''
        def check_callback(is_already):
            self.switch.set_active(is_already)
            self.switch.set_sensitive(True)
            
        def enable_widget_callback():
            self.label.set_sensitive(True)
            self.wrapper.check(check_callback)
            
        self.wrapper.enable(enable_widget_callback)
