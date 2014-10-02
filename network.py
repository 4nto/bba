import re, subprocess, pkg_resources
import netifaces as NI
from batch import Batch
from util import command_exist, version_cmp, get_default_gateway_linux

assert command_exist ("/usr/bin/macchanger")
assert command_exist ("anonymous")

class NetworkInterfaces(Batch):
    script_anonymous = 'anonymous'
    cmd_check = 'macchanger -s '
    selected = None
    timeout = 30000 #milliseconds
    
    def __init__(self, log, output):
        self.log = log.getChild(__name__)
        Batch.__init__ (self, self.log)
        self.set_writer (output)
        self.pattern = re.compile (r"([0-9A-F]{2}[:-]){5}([0-9A-F]{2})", re.I)
        self.set_script(self.script_anonymous)
        self.update()

    def update(self):
        '''Do not consider "lo" interface and interface without physical addr (virtual)'''
        self.interfaces = filter (lambda i: i != "lo" and NI.AF_LINK in NI.ifaddresses(i), NI.interfaces()) 
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
        
    def get_addr(self, iname):
        return self.ifaddresses[iname] if iname in self.ifaddresses.keys() else None        

    def select (self, ifname):
        self.selected = ifname

    def check (self, callback):
        assert self.selected is not None
        def parser (exit_code, stdout):
            try:
                macs = map (lambda line: self.pattern.search(line).group(), stdout.strip().splitlines())
            except:
                self.log.error ("Parsing error")
                callback (False)                
            else:
                callback (macs[1:] != macs[:-1])
                        
        self.set_cmd (self.cmd_check + self.selected, should_be_root = False)
        self.set_callback (parser)
        self.ipc_pipe_based()

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
        
    def set_script (self, script):
        self.script_anonymous = script
        self.cmd_set = script + ' start -m '
        self.cmd_reset = script + ' stop -m '
