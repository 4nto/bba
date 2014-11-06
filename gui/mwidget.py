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
            image.set_from_file(wrapper.config.get('config', 'button'))
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

    def connect_wrapper(self):
        '''Connect widget signals to the functions managed by the wrapper'''                    
        def connect_wrapper_switch(widget, *args):
            def check_callback(is_already):
                self.control.set_active(is_already)
                self.control.set_sensitive(True)
                
            def callback(*args):            
                self.wrapper.check(check_callback)
                
            widget.set_sensitive(False)
            if widget.get_active():
                self.wrapper.stop(callback)
            else:
                self.wrapper.start(callback)                                               
                    
        def connect_wrapper_button(widget, *args):
            def check_callback(is_already):
                self.control.set_sensitive(is_already)
                
            def callback(*args):            
                self.wrapper.check(check_callback)
                
            widget.set_sensitive(False)
            self.wrapper.start(callback)                                                           
            
        self.control.connect('button-press-event', connect_wrapper_button\
                             if self.button else connect_wrapper_switch)

    def verify_and_enable(self):
        '''Makes enable the widget'''                
        def enable_widget_switch(sensitive):
            def check_callback(is_already):
                self.control.set_active(is_already)
                self.control.set_sensitive(sensitive)
                
            self.label.set_sensitive(True)
            self.wrapper.check(check_callback)                            
            
        def enable_widget_button(sensitive):
            def check_callback(is_already):
                self.control.set_sensitive(True)
                
            self.label.set_sensitive(True)
            self.wrapper.check(check_callback)

        if self.button:
            self.wrapper.verify(enable_widget_button)
        else:
            self.wrapper.verify(enable_widget_switch)
            

