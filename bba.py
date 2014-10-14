#!/usr/bin/env python
__author__ = 'Antonio De Rosa'

import os
from gi.repository import Gtk
from gui import GUI, PanedSwitchLabel, WrappedFileChooserDialog
from util.configuration import Configurator
from util.wrapper import Wrapper
from util import __version__, __python_version__, __gtk_version__, __license__

import network.setup

class BBA(GUI):
    def __init__ (self, glade_file, log_file, css_file):
        GUI.__init__ (self, glade_file, log_file, css_file)
        self.tv = self.get_object("textview1")        
        self.write_in_textview = lambda text: self.tv.get_buffer().insert(self.tv.get_buffer().get_end_iter(), text)

        for module in self.__get_modules():
            wrapper = Wrapper (self.log, self.write_in_textview, module)
            paned = PanedSwitchLabel(wrapper)                                                                    
            paned.connect_wrapper()            
            self.get_object("box1").pack_start(paned, expand = False, fill = True, padding = 5)            
        
    def __get_modules(self):
        config = Configurator('bba.cfg')
        for module in config.items('modules'):
            if module[0] in config.items('dynamic')[0]:
                for fname in filter (lambda fname: module[0] + '-' in fname, os.listdir(module[0])):
                    yield "{}/{}".format(module[0], fname)
            else:                
                yield "{0}/{0}.cfg".format(module[0])       

    #autoscroll
    def on_textview_sizeallocate_event (self, textview, *args):
        adj = textview.get_vadjustment()
        adj.set_value(adj.get_upper() - adj.get_page_size())

    def on_menu_about_activate (self, *args):
        dialog = Gtk.MessageDialog (self.get_object("window"),
                                    0,
                                    Gtk.MessageType.INFO,
                                    Gtk.ButtonsType.OK,
                                    "BackBox Anonymizer")

        text = [__version__, __python_version__, __gtk_version__, '', __license__]        
        dialog.format_secondary_text ("\n".join (text))
        
        dialog.run()
        dialog.destroy()

    def on_menu_file_save_activate (self, *args):
        with WrappedFileChooserDialog ("Please choose a file",
                                       self.get_object("window"),
                                       Gtk.FileChooserAction.SAVE,
                                       (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, "Select", Gtk.ResponseType.OK)) as fcd:

            if fcd['response'] == Gtk.ResponseType.OK:
                with open(fcd['dialog'].get_filename(), 'w') as f:
                    f.write(self.tv.get_buffer().get_text(self.tv.get_buffer().get_start_iter(),
                                                          self.tv.get_buffer().get_end_iter(),
                                                          True))

                self.log.warning("Saved application log into {}".format(fcd['dialog'].get_filename()))       

    def on_menu_clear_activate (self, *args):
        self.tv.get_buffer().delete(self.tv.get_buffer().get_start_iter(), self.tv.get_buffer().get_end_iter())
    
if __name__ == '__main__':
    bba = BBA("gui/gui6.glade", "bba.log", "gui/style.css")
    bba()        
