#!/usr/bin/env python
'''Main file'''
__author__ = 'Antonio De Rosa'

import os
from gi.repository import Gtk
from gui import GUI, PanedSwitchLabel, WrappedFileChooserDialog
from util.configuration import Configurator
from util.wrapper import Wrapper
from util import __version__, __python_version__, __gtk_version__, __license__

import network.setup

class BBA(GUI):
    '''Main Class'''
    def __init__ (self):
        '''BBA Class Constructor'''
        self.config = Configurator('bba.cfg')
        GUI.__init__ (self,
                      self.config.get('config', 'glade'),
                      self.config.get('config', 'log'),
                      self.config.get('config', 'css'))
        
        self.tv = self.get_object("textview1")
        self.box1 = self.get_object("box1")
        self.box2 = self.get_object("box2")
        self.w_tv = lambda text: self.tv.get_buffer().insert(self.tv.get_buffer().get_end_iter(), text)

        for module in self.__get_modules():
            wrapper = Wrapper (self.log, self.w_tv, module)
            if wrapper.check_dependences():
                paned = PanedSwitchLabel(wrapper)
                box = self.box2 if wrapper.config.getboolean('config', 'hide')\
                    else self.box1
                box.pack_start(paned, expand = False, fill = True, padding = 5)
                paned.connect_wrapper()

        if not self.box2.get_children():
            self.get_object("expander").hide()
        
    def __get_modules(self):
        '''Return all the configuration files from the modules dir'''
        for module in self.config.items('modules'):
            if module[0] in self.config.items('dynamic')[0]:
                for fname in filter (lambda fname: module[0] + '-' in fname,
                                     os.listdir(module[0])):
                    yield "{}/{}".format(module[0], fname)
            else:                
                yield "{0}/{0}.cfg".format(module[0])       

    def on_textview_sizeallocate_event (self, textview, *args):
        '''Provide autoscrolling for the textview'''
        adj = textview.get_vadjustment()
        adj.set_value(adj.get_upper() - adj.get_page_size())

    def on_menu_about_activate (self, *args):
        '''Show About form'''
        dialog = Gtk.MessageDialog (self.get_object("window"),
                                    0,
                                    Gtk.MessageType.INFO,
                                    Gtk.ButtonsType.OK,
                                    "BackBox Anonymizer")

        text = [__version__,
                __python_version__,
                __gtk_version__,
                __license__]
        
        dialog.format_secondary_text ("\n".join (text))
        
        dialog.run()
        dialog.destroy()

    def on_menu_file_save_activate (self, *args):
        '''Show File Save form'''
        with WrappedFileChooserDialog ("Please choose a file",
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

    def on_menu_clear_activate (self, *args):
        '''Clear the textview'''
        self.tv.get_buffer().delete(self.tv.get_buffer().get_start_iter(),
                                    self.tv.get_buffer().get_end_iter())
    
if __name__ == '__main__':
    bba = BBA()
    bba()        
