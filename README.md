BackBox Anonymizer
==============

Simply anonymize your network and web activities through Tor and other open-source tools <br />

BBA works on Linux, it is tested with [BackBox Linux](www.backbox.org) and Ubuntu <br />

BBA is made by modules, each one provides an indipendent function and you can easily create your own by following [related doc](doc/Modules.md) <br />


It is developed in Python with GTK+3

![Linux](http://img.shields.io/badge/OS-Linux-blue.svg)&nbsp; 
![GTK](http://img.shields.io/badge/GUI-GTK+3-yellow.svg)&nbsp; 
![Python](http://img.shields.io/badge/Language-Python-green.svg)&nbsp; 
![License](http://img.shields.io/badge/License-GNU_GPL_2.0-red.svg)&nbsp; 

Run
--------------
Download and extract [ZIP file](https://github.com/4nto/bba/archive/master.zip) then launch bba.py

If you launch it as unprivileged user you can only see the system information 

Dependecies
--------------
BBA needs Python 2.7 and Gtk+3 (tested with 3.4 and 3.10 versions), if you click on Help > Information you will discover the version used in your system.<br />

The following tools are necessary for the current standard modules: 

* [Tor](https://www.torproject.org/) to surf anonymously
* [Bleachbit](http://bleachbit.sourceforge.net/) clean your system
* [GNU Macchanger](http://www.gnu.org/software/macchanger/) change your physical address
* [virt-what](http://people.redhat.com/~rjones/virt-what/) (optional) detect if you are running on virtualized environment
```sh
sudo apt-get install tor bleachbit macchanger virt-what 
```

