import re, subprocess, pkg_resources
import netifaces as NI
from batch import Batch
from util import version_cmp, command_exist

# netifaces version must be greater than 0.10.4
assert version_cmp (pkg_resources.get_distribution("netifaces").version, "0.10.4") >= 0
assert command_exist ("/usr/bin/macchanger")
assert command_exist ("/usr/sbin/anonymous")

class NetworkInterfaces(Batch):
    cmd_set = 'sh ../backbox-anonymous/usr/sbin/anonymous start -m '
    cmd_reset = 'sh ../backbox-anonymous/usr/sbin/anonymous stop -m '
    cmd_check = 'macchanger -s '
    selected = None
    
    def __init__(self, log, output):
        self.log = log.getChild(__name__)
        Batch.__init__ (self, self.log)
        self.set_writer (output)
        self.pattern = re.compile (r"([0-9A-F]{2}[:-]){5}([0-9A-F]{2})", re.I)
        self.update()

    def update(self):
        self.interfaces = NI.interfaces()
        self.ifaddresses = {i:NI.ifaddresses(i)[NI.AF_LINK][0]['addr'] for i in self.interfaces}
        
        if NI.gateways()['default'].has_key(NI.AF_INET):
            self.default_gw = NI.gateways()['default'][NI.AF_INET][1]
        else:
            self.default_gw = self.interfaces[-1]
            self.log.warning ("Unable to find default gateway, using {} instead".format(self.default_gw))  

    def get_interfaces (self):
        return self.interfaces
        
    def get_default (self):
        return self.default_gw
        
    def get_addr(self, iname):
        return self.ifaddresses[iname] if iname in self.ifaddresses.keys() else None        

    def select (self, ifname):
        self.selected = ifname

    def check (self, callback):
        def parser (fd):
            self.log.error ("test parsing!")
            try:
                macs = map (lambda line: self.pattern.search(line).group(), fd.readlines())
            except:
                self.log.error ("Parsing error")
                callback (False)                
            else:
                callback (macs[1:] != macs[:-1])
                        
        self.set_cmd (self.cmd_check + self.selected, should_be_root = False)
        self.set_callback (parser)
        self.run_and_parse()

    def set(self, iface, callback):                
        self.set_cmd (self.cmd_set + iface)
        self.set_callback (callback)
        self.run()

    def reset(self, iface, callback):
        self.set_callback (callback)
        self.set_cmd (self.cmd_reset + iface)
        self.run()
