#!/usr/bin/env python
'''Get from the torproject webpage if you are using Tor'''

from __future__ import print_function
import urllib2
import sys
import re

def check():
    pattern = re.compile (r'[0-9]+(?:\.[0-9]+){3}', re.I)
    result = urllib2.urlopen('https://check.torproject.org/?lang=en_US')
    lines = result.readlines()
    IPline = filter(lambda line: "IP address" in line, lines)
    IP = pattern.search(IPline[0]).group() if len(IPline) == 1 else 'n/a'
    if filter (lambda line: 'Congratulations. This' in line, lines) == []:
        print("Sorry but you {} are not using Tor".format(IP))
        sys.exit(1)

    print("Congratulation, you are using Tor as {}".format(IP))

try:
    check()
except KeyboardInterrupt:
    print("Unable to retrieve your IP")    
    print("SIGINT received (timeout or CTRL+C)", file=sys.stderr)
    sys.exit(2)
except (urllib2.HTTPError, urllib2.URLError):
    print("Unable to retrieve your IP")    
    print("Unable to retrieve URL", file=sys.stderr)
    sys.exit(2)
except Exception as inst:
    print("Unable to retrieve your IP")
    print("Unknown_error: {}".format(inst), file=sys.stderr)
    sys.exit(2)
