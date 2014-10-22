#!/usr/bin/env python
'''Main file'''
__author__ = 'Antonio De Rosa'

import os
import ConfigParser
from gi.repository import Gtk

import gui 
import gui.mwidget
import util.setup
import util.wrapper
from util import __version__, __python_version__, __gtk_version__, __license__

class BBA(gui.GUI):
    '''Main Class'''
    def __init__(self, config_fname):
        '''BBA Class Constructor'''
        self.config = ConfigParser.SafeConfigParser(allow_no_value = True)
        self.config.read(config_fname)
        gui.GUI.__init__(self,
                         self.config.get('config', 'glade'),
                         self.config.get('config', 'log'),
                         self.config.get('config', 'css'))
        
        self.tv = self.get_object("textview1")
        self.box1 = self.get_object("box1")
        self.box2 = self.get_object("box2")        
        self.w_tv = lambda text: self.tv.get_buffer().insert\
                   (self.tv.get_buffer().get_end_iter(), text)

        if os.getuid() == 0:
            self.get_object("warning").hide()
        
        def load_widget_module(name, conf):
            '''Create a single module/widget'''
            wrapper = util.wrapper.Wrapper(log = self.log,
                                           output = self.w_tv,
                                           config = conf,
                                           name = name)
            
            paned = gui.mwidget.PanedWidget(wrapper,
                                            conf.has_option('config', 'button'))
            
            box = self.box2 if conf.getboolean('config', 'hide') else self.box1
            
            box.pack_start(paned, expand = False, fill = True, padding = 5)
            
            if self.box2.get_children():
                self.get_object("expander").show()

            paned.connect_wrapper()                
            paned.verify_and_enable()

        inst = lambda mod: util.setup.configure_module(mod[0],
                                                       load_widget_module,
                                                       self.log)
        map(inst, self.config.items('modules'))
                                                   
    def on_textview_sizeallocate_event(self, textview, *args):
        '''Provide autoscrolling for the textview'''
        adj = textview.get_vadjustment()
        adj.set_value(adj.get_upper() - adj.get_page_size())

    def on_menu_about_activate(self, *args):
        '''Show About form'''
        dialog = Gtk.MessageDialog(self.get_object("window"),
                                    0,
                                    Gtk.MessageType.INFO,
                                    Gtk.ButtonsType.OK,
                                    "BackBox Anonymizer")

        text = [__version__,
                __python_version__,
                __gtk_version__,
                __license__]
        
        dialog.format_secondary_text("\n".join(text))
        
        dialog.run()
        dialog.destroy()

    def on_menu_file_save_activate(self, *args):
        '''Show File Save form'''
        with gui.WrappedFileChooserDialog("Please choose a file",
                                          self.get_object("window"),
                                          Gtk.FileChooserAction.SAVE,
                                          (Gtk.STOCK_CANCEL,
                                           Gtk.ResponseType.CANCEL,
                                           "Select",
                                           Gtk.ResponseType.OK)) as fcd:

            if fcd['response'] == Gtk.ResponseType.OK:
                fname = fcd['dialog'].get_filename()
                with open(fname, 'w') as save:
                    start = self.tv.get_buffer().get_start_iter()
                    end = self.tv.get_buffer().get_end_iter()
                    save.write(self.tv.get_buffer().get_text(start, end, True))

                self.log.warning("Saved application log into {}".format(fname))

    def on_menu_clear_activate(self, *args):
        '''Clear the textview'''
        self.tv.get_buffer().delete(self.tv.get_buffer().get_start_iter(),
                                    self.tv.get_buffer().get_end_iter())
    
if __name__ == '__main__':
    instance = BBA('bba.cfg')
    instance()        
