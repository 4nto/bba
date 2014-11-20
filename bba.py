#!/usr/bin/env python
'''Main file'''
__author__ = 'Antonio De Rosa'

import os
import sys
import ConfigParser

# to avoid unity MENUPROXY hide the menubar
if 'UBUNTU_MENUPROXY' in os.environ:
    os.environ['UBUNTU_MENUPROXY'] = "0"

from gi.repository import Gtk, GObject

from gui import GUI
from gui.mwidget import PanedWidget
import util.setup
from util.wrapper import Wrapper

class BBA(GUI):
    '''Main Class'''
    def __init__(self, config_fname):
        '''BBA Class Constructor'''
        config = ConfigParser.SafeConfigParser(allow_no_value = True)
        config.read(config_fname)
        super(BBA, self).__init__(config.get('config', 'glade'),
                                  config.get('config', 'log'),
                                  config.get('config', 'css'))

        self.config_fname = config_fname
        self.tv = self.get_object("textview1")
        self.progressbar_step = 0
        
        self.tv.get_buffer().create_tag("warning", foreground = 'red')
        self.tv.get_buffer().create_tag("check", weight = 700)
        self.tv.get_buffer().create_tag("toggle_module", foreground = 'blue', weight = 700)
        
        box1 = self.get_object("box1")
        box2 = self.get_object("box2")
        submenu_modules = self.get_object('submenu_modules')
        progressbar = self.get_object("progressbar")        
        modules = filter(lambda d: os.path.isdir('modules/' + d),
                         os.listdir('modules'))

        def on_timeout(user_data):
            progressbar.set_fraction(progressbar.get_fraction() + self.progressbar_step)
            return True
            
        GObject.timeout_add(1000, on_timeout, None)

        if os.getuid() == 0:
            self.get_object("warning").hide()

        def lock_operations(enable, module, timeout, halt):
            '''Avoid the access to other start/stop operations'''
            progressbar.set_fraction(0)   
            self.progressbar_step = 1000/float(timeout) if enable else 0
            progressbar.set_text("Running {} module..".format(module))
            getattr(self.get_object("info"), 'show' if enable else 'hide')()            
            box1.set_sensitive(not enable)
            box2.set_sensitive(not enable)
            self.get_object('button_stop').connect('clicked', halt)
            

        def load_module(module):
            '''
            Load a single module, if it is enabled creates the related widget
            else shows only the menu item
            '''
            def load_widget_module(name, conf):
                '''Create the internal logic of a module/widget'''
                wrapper = Wrapper(log = self.log,
                                  config = conf,
                                  name = name,
                                  output = self.write,
                                  info = lambda t: self.write(t, 'check'),
                                  warning = lambda t: self.write(t, 'warning'))
                
                paned = PanedWidget(wrapper, conf.has_option('config', 'button'))
                
                box = box2 if conf.getboolean('config', 'hide') else box1
                
                box.pack_start(paned, expand = False, fill = True, padding = 5)
                
                if box2.get_children():
                    self.get_object("expander").show()

                paned.verify_and_connect(lock_operations)
            
            def toggle_menu_module(item):
                '''Insert a module into the menu bar'''
                config.set('modules', item.get_label(), str(item.get_active()))
                self.write("At the next start module {} will be {}\n"\
                          .format(item.get_label(), "enabled" \
                          if item.get_active() else "disabled"),
                          tag = 'toggle_module')
                
                with open(config_fname, 'wb') as fd:
                    config.write(fd)
                    
            moduleItem = Gtk.CheckMenuItem(module)
            moduleItem.set_draw_as_radio(True)
            
            if module in config.options('modules') and config.getboolean('modules', module):
                util.setup.configure_module(module, load_widget_module, self.log)
                moduleItem.set_active(True)
                            
            submenu_modules.add(moduleItem)
            moduleItem.connect('toggled', toggle_menu_module)
            moduleItem.show()            
        
        map(load_module, modules)        

    def write(self, text, tag = None):
        textbuffer = self.tv.get_buffer()
        start = textbuffer.get_end_iter()
        
        if tag:
            textbuffer.insert_with_tags_by_name(start, text, tag)
        else:
            textbuffer.insert(start, text)
                
    
    def on_textview_sizeallocate_event(self, textview, *args):
        '''Provide autoscrolling for the textview'''
        adj = textview.get_vadjustment()
        adj.set_value(adj.get_upper() - adj.get_page_size())

    def on_menu_file_save_activate(self, dialog):
        '''Show File Save form'''
        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            fname = dialog.get_filename()
            with open(fname, 'w') as save:
                start = self.tv.get_buffer().get_start_iter()
                end = self.tv.get_buffer().get_end_iter()
                save.write(self.tv.get_buffer().get_text(start, end, True))

            self.log.warning("Saved application log into {}".format(fname))
            
        dialog.hide()

    def on_menu_clear_activate(self, *args):
        '''Clear the textview'''
        self.tv.get_buffer().delete(self.tv.get_buffer().get_start_iter(),
                                    self.tv.get_buffer().get_end_iter())
    
if __name__ == '__main__':
    instance = BBA('modules/bba.cfg')
    instance()        
