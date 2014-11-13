#!/usr/bin/env python
'''Main file'''
__author__ = 'Antonio De Rosa'

import os
import sys
import ConfigParser

# to avoid unity MENUPROXY hide the menubar
if 'UBUNTU_MENUPROXY' in os.environ:
    os.environ['UBUNTU_MENUPROXY'] = "0"

from gi.repository import Gtk

import gui 
import gui.mwidget
import util.setup
import util.wrapper

class BBA(gui.GUI):
    '''Main Class'''
    def __init__(self, config_fname):
        '''BBA Class Constructor'''
        config = ConfigParser.SafeConfigParser(allow_no_value = True)
        config.read(config_fname)
        super(BBA, self).__init__(config.get('config', 'glade'),
                                  config.get('config', 'log'),
                                  config.get('config', 'css'))

        self.config_fname = config_fname
        tview = self.get_object("textview1")
        box1 = self.get_object("box1")
        box2 = self.get_object("box2")
        submenu_modules = self.get_object('submenu_modules')
        
        self.w_tv = lambda text: tview.get_buffer().insert\
                   (tview.get_buffer().get_end_iter(), text)
        
        def load_widget_module(name, conf):
            '''Create a single module/widget'''
            wrapper = util.wrapper.Wrapper(log = self.log,
                                           output = self.w_tv,
                                           config = conf,
                                           name = name)
            
            paned = gui.mwidget.PanedWidget(wrapper,
                                            conf.has_option('config', 'button'))
            
            box = box2 if conf.getboolean('config', 'hide') else box1
            
            box.pack_start(paned, expand = False, fill = True, padding = 5)
            
            if box2.get_children():
                self.get_object("expander").show()

            paned.verify_and_connect()

        def load_module(module):
            def toggle_menu_module(item):
                config.set('modules', item.get_label(), str(item.get_active()))
                self.w_tv("At the next start module {} will be {}\n"\
                          .format(item.get_label(), "enabled" \
                          if item.get_active() else "disabled"))
                
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

        modules = filter(lambda d: os.path.isdir('modules/' + d),
                         os.listdir('modules'))
        
        map(load_module, modules)
            
        if os.getuid() == 0:
            self.get_object("warning").hide()            
                                                   
    def on_textview_sizeallocate_event(self, textview, *args):
        '''Provide autoscrolling for the textview'''
        adj = textview.get_vadjustment()
        adj.set_value(adj.get_upper() - adj.get_page_size())

    def on_menu_about_activate(self, dialog):
        '''Show About form'''
        dialog.run()
        dialog.hide()
        '''
        "Python v" + ".".join (map (str, sys.version_info[:3])),
        "GTK v{}.{}.{}".format (Gtk.get_major_version(),
                                        Gtk.get_minor_version(),
                                        Gtk.get_micro_version()),'',
        '''
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
