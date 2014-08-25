BackBox Anonymizer
==============

A simple GUI to anonymize your web activities by mixing Tor, Bleachbit and GNU Macchanger. <br />

BBA works on Linux and is developed in python with GTK3/GObject, it is based on backbox-anonymous script

![Linux](http://img.shields.io/badge/OS-Linux-blue.svg)
![GTK](http://img.shields.io/badge/GUI-GTK-yellow.svg)
![Python](http://img.shields.io/badge/Language-Python-green.svg) 
![License](http://img.shields.io/badge/License-GNU_GPL_2.0-red.svg)
![version RC0](http://img.shields.io/badge/Version-RC0-lightgrey.svg)

Run
--------------
Download ZIP file then launch ./bba.py

Dependecies
--------------
* [**backbox anonymous**](https://github.com/4nto/backbox-anonymous) <br />
BackBox Script for Anonymous Internet Navigation
```sh
wget -c https://raw.githubusercontent.com/4nto/backbox-anonymous/master/usr/sbin/anonymous
chmod +x anonymous
mv anonymous /usr/sbin/anonymous
```
* [Tor](https://www.torproject.org/), [Bleachbit](http://bleachbit.sourceforge.net/), [GNU Macchanger](http://www.gnu.org/software/macchanger/), and [Python Netifaces](https://pypi.python.org/pypi/netiface)
```sh
sudo apt-get install tor bleachbit macchanger python-netifaces
```
