#!/usr/bin/env python
'''Main file'''
__author__ = 'Antonio De Rosa'

from gi.repository import Gtk
from gui import GUI, PanedSwitchLabel, WrappedFileChooserDialog
from util.configuration import Configurator
from util.wrapper import Wrapper
from util.batch import Batch
from util import __version__, __python_version__, __gtk_version__, __license__

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
        self.w_tv = lambda text: self.tv.get_buffer().insert\
                    (self.tv.get_buffer().get_end_iter(), text)
        
        box1 = self.get_object("box1")
        box2 = self.get_object("box2")

        setup = Batch(self.log)        

        def configure_module(module):
            '''
            SETUP STEP
            Run in a separate process the setup script which creates
            eventually more dynamic config files
            If it returns an error don't show the related widget/s
            If there is no setup script use the default config file
            '''
            def load_widget_module(configurator):
                '''Create a single module/widget'''
                wrapper = Wrapper (self.log, self.w_tv, configurator)
                paned = PanedSwitchLabel(wrapper)
                box = box2 if wrapper.config.getboolean('config', 'hide')\
                      else box1
                box.pack_start(paned, expand = False, fill = True, padding = 5)
                if box2.get_children():
                    self.get_object("expander").show()

                paned.connect_wrapper()
                paned.enable_widget()

            def run_setup_script(cmd):
                '''Run in background the setup script'''
                def setup_callback(exit_code, stdout):
                    '''Callback launched at the end of the setup script'''
                    if exit_code == 0:
                        for line in stdout.splitlines():
                            dconfig = Configurator(line)
                            load_widget_module(dconfig)
                    else:
                        self.log.error("Error setting up the module {}:{}"\
                                       .format(module, stdout))
                        
                setup.set_cmd(cmd, should_be_root = False)                    
                setup.set_callback(setup_callback)
                setup.ipc_pipe_based(mconfig.getint('config', 'timeout'))
                    
            try:
                mconfig = Configurator("{0}/{0}.cfg".format(module))
            except:
                self.log.error("No configuration file for module {}"\
                               .format(module))
            else:
                try:
                    fsetup = mconfig.get('config', 'setup')
                except:
                    self.log.warning("No setup file for module {}"\
                                     .format(module))
                    load_widget_module(mconfig)
                else:                    
                    run_setup_script(fsetup)
        
        map(lambda mod: configure_module(mod[0]), self.config.items('modules'))

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
