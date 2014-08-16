BackBox Anonymizer
==============

A simple GUI for backbox-anonymous script to anonymize your web activities by mixing Tor, Bleachbit and GNU Macchanger. <br />

BBA works on Linux and is developed in python with GTK3/GObject.

Dependecies
--------------

* [backbox anonymous](https://github.com/4nto/backbox-anonymous)
```
wget -c https://raw.githubusercontent.com/4nto/backbox-anonymous/master/usr/sbin/anonymous
chmod +x anonymous
mv anonymous /usr/sbin/anonymous
```
* [Tor](https://www.torproject.org/), [bleachbit](http://bleachbit.sourceforge.net/), [macchanger](http://www.gnu.org/software/macchanger/), and [Python Netifaces](https://pypi.python.org/pypi/netiface)
```
sudo apt-get install tor bleachbit macchanger python-netifaces
```
