from gi.repository import Gtk

class PanedWidget(Gtk.Paned):
    def __init__(self, wrapper, button = False):
        '''Create the combination switch/label or button/label in the paned'''
        super(PanedWidget, self).__init__()
        self.wrapper = wrapper
        self.button = button
        
        self.set_position(100)
        self.label = Gtk.Label(wrapper.config.get('config', 'title'))
        self.label.set_halign(Gtk.Align.START)
        self.label.set_sensitive(False)

        if button:
            self.control = Gtk.Button()
            image = Gtk.Image()
            image.set_from_file(wrapper.cwd(wrapper.config.get('config',
                                                               'button')))
            self.control.add(image)
        else:
            self.control = Gtk.Switch()
            self.control.set_active(False)        
            
        self.control.set_size_request(72, 30)
        self.control.set_sensitive(False)
        self.control.set_margin_left(10)
        self.control.set_margin_right(20)
        self.control.set_valign(Gtk.Align.CENTER)
        self.control.set_halign(Gtk.Align.CENTER)
        
        self.add1(self.control)
        self.add2(self.label)
        self.show_all()

    def connect_wrapper(self, lock):
        wlock = lambda enable: lock(enable,
                                    self.wrapper.name,
                                    self.wrapper.config.get('config', 'timeout'),
                                    self.wrapper.halt)
        
        '''Connect widget signals to the functions managed by the wrapper'''
        def check_callback_switch(is_already):
                self.control.set_active(is_already)
                self.control.set_sensitive(True)
            
        def connect_wrapper_switch(widget, *args):                
            def callback(*args):
                wlock(False)
                self.wrapper.check(check_callback_switch)
                
            widget.set_sensitive(False)
            wlock(True)
            if widget.get_active():
                self.wrapper.stop(callback)
            else:
                self.wrapper.start(callback)                                    

        def check_callback_button(is_already):            
            self.control.set_sensitive(is_already)
                    
        def connect_wrapper_button(widget, *args):                
            def callback(*args):
                wlock(False)
                self.wrapper.check(check_callback_button)
                
            widget.set_sensitive(False)
            wlock(True)
            self.wrapper.start(callback)
            
        self.control.connect('button-press-event', connect_wrapper_button\
                             if self.button else connect_wrapper_switch)

        self.wrapper.check(check_callback_button if self.button else\
                           check_callback_switch)

    def  verify_and_connect(self, lock):
        def enable_and_connect(enabled):
            self.label.set_sensitive(enabled)
            self.control.set_sensitive(enabled)
            
            if enabled:        
                self.connect_wrapper(lock)
            else:
                self.wrapper.check(lambda b: None)

        self.wrapper.verify(enable_and_connect)
            

