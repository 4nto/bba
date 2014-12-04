BackBox Anonymizer
==============

Simply anonymize your network and web activities through Tor and other open-source tools <br />

BBA works on Linux, it is tested with [BackBox Linux](https://www.backbox.org) and Ubuntu 14.04 <br />

BBA is made by modules, each one provides an indipendent function and you can easily create your own by following [related doc](doc/Modules.md#making-a-new-module)<br />

It is developed in Python with GTK+3

![Linux](http://img.shields.io/badge/OS-Linux-blue.svg)&nbsp; 
![GTK](http://img.shields.io/badge/GUI-GTK+3-yellow.svg)&nbsp; 
![Python](http://img.shields.io/badge/Language-Python-green.svg)&nbsp; 
![License](http://img.shields.io/badge/License-GNU_GPL_2.0-red.svg)&nbsp; 

Run
--------------
Download and extract [ZIP file](https://github.com/4nto/bba/archive/master.zip) then launch bba.py

If you launch it as unprivileged user you can only see the system information 

If you want use the desktop entry edit in bba-root.desktop the Exec and Icon entries with absoulute path

Dependecies
--------------
BBA needs Python 2.7 and Gtk+3 already present in recent Linux distributions. If you click on Help > Information you will discover the version used in your system <br />

The [default modules](doc/Modules.md#default-modules) need the following tools

```sh
sudo apt-get install tor bleachbit macchanger virt-what 
```
