BackBox Anonymizer
==============

A simple GUI to anonymize your web activities by mixing Tor, Bleachbit and GNU Macchanger. <br />

It is designed to be modular, you can create your own plug-in by following [documentation](doc/Modules.md). <br />

BBA works on Linux and is developed in Python with GTK+3, proudly based on [backbox-anonymous](https://github.com/raffaele-forte/backbox-anonymous) script

![Linux](http://img.shields.io/badge/OS-Linux-blue.svg)&nbsp; 
![GTK](http://img.shields.io/badge/GUI-GTK-yellow.svg)&nbsp; 
![Python](http://img.shields.io/badge/Language-Python-green.svg)&nbsp; 
![License](http://img.shields.io/badge/License-GNU_GPL_2.0-red.svg)&nbsp; 
![version 1.0](http://img.shields.io/badge/Version-1.0-lightgrey.svg)&nbsp; 

Run
--------------
Download ZIP file then launch ./bba.py or python bba.py

If you launch it as unprivileged user you can only see the system information 

Dependecies
--------------
* [Tor](https://www.torproject.org/) to surf anonymously
* [Bleachbit](http://bleachbit.sourceforge.net/) to clean your system
* [GNU Macchanger](http://www.gnu.org/software/macchanger/) to change your physical address
* [virt-what](http://people.redhat.com/~rjones/virt-what/) (optional) to detect if you are running on virtualized environment
```sh
sudo apt-get install tor bleachbit macchanger virt-what 
```

