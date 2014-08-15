import re, subprocess, pkg_resources
import netifaces as NI
from batch import Batch
from util import command_exist, version_cmp, get_default_gateway_linux

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
        self.interfaces = filter (lambda i: i != "lo", NI.interfaces()) # don't consider lo interface
        self.ifaddresses = {i:NI.ifaddresses(i)[NI.AF_LINK][0]['addr'] for i in self.interfaces}

        # netifaces version must be greater than 0.10.4
        if version_cmp (pkg_resources.get_distribution("netifaces").version, "0.10.4") >= 0:
            if NI.gateways()['default'].has_key(NI.AF_INET):
                self.default_gw = NI.gateways()['default'][NI.AF_INET][1]
            else:
                self.default_gw = None # self.interfaces[-1]
        else:
            self.default_gw = get_default_gateway_linux()

        if self.default_gw is None:
            self.log.warning ("Unable to find default gateway..".format(self.default_gw))
            
    def get_interfaces (self):
        return self.interfaces
        
    def get_default (self):
        return self.default_gw
        
    def get_addr(self, iname):
        return self.ifaddresses[iname] if iname in self.ifaddresses.keys() else None        

    def select (self, ifname):
        self.selected = ifname

    def check (self, callback):
        assert self.selected is not None
        def parser (fd):
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

    def set (self, callback):
        assert self.selected is not None
        self.set_cmd (self.cmd_set + self.selected)
        self.set_callback (callback)
        self.run()

    def reset (self, callback):
        assert self.selected is not None
        self.set_cmd (self.cmd_reset + self.selected)
        self.set_callback (callback)
        self.run()
