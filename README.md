BackBox Anonymizer
==============

Simply anonymize your network and web activities through Tor and other open-source tools <br />

BBA is made by modules, each one provides an indipendent function and you can easily create your own by following [related doc](doc/Modules.md) <br />

BBA works on Linux, it is designed for [BackBox Linux](www.backbox.org) and Ubuntu (14.04) but it works also on other Debian-based distro

It is developed in Python with GTK+3

![Linux](http://img.shields.io/badge/OS-Linux-blue.svg)&nbsp; 
![GTK](http://img.shields.io/badge/GUI-GTK+3-yellow.svg)&nbsp; 
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

