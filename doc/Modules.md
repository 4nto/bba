#Modules

A module is an indipendent python script which performs a simple operation which could be represent by a Switch or a Button. A switch is a module with start/stop/check operations while a button represents a module with only start/check operations.<br/>

Every is only avilable by command line, as example by running
```
./module/bleachbit/check.py
```
I can see how many files the script start.py will remove from my system (related to the options in bleachbit.cfg file).

The GUI use the modules through ini-like configuration files that have a well-defined key-words, following you will find them.

In the current BBA version the default modules are

1.  **bleachbit** to clean the system by using bleachbit 
2.  **hostname** to randomize and restore the system hostname
3.  **network** to randomize and restore the MAC address for each physical network interface (but not in virtual machine)
4.  **tor** to transparently route traffic through Tor

##Making a new module
* Create a new directory and name it as your module, e.g. **MyModule**
* Put the directory **MyModule** into *modules/*
* Into your new directory create the configuration file and name it **MyModule.cfg**

##Configuration File
Following an example of configuration file, [here](https://wiki.python.org/moin/ConfigParserExamples) you will find some examples. <br/>
It have to contain at least the sections **[config]** and  **[cmd]**  with the options

* **[config] title**: the description showed in the gui left to gtk command
* **[config] hide**: if the gtk command have to be showed (True) in the *main list* or in the *more list* of the GUI (False)
* **[config] root**: start/stop operations have to run as root? (True/False)
* **[config] timeout**: the timeout [ms] for the check/start/stop operations
* **[cmd] check**: the name of the executable contained in the module directory which performs the check operation
* **[cmd] start**: the name of the executable contained in the module directory which performs the start operation

and optionally

* **[config] assert:** a list of comma-separated string (without spaces) of the needed binary
* **[config] button:** specified if the module performs a start/check operation, it contains optionally the icon name used in the gtk button
* **[config] setup:** the name of the executable contained in the module directory which performs the SETUP phase
* **[cmd] stop:** the name of the executable contained in the module directory which performs the stop operation
* **[cmd] init:** the name of the executable contained in the module directory which performs the VERIFY phase


```
#Bleachbit Module Configuration File
[DEFAULT]
cleaners:   bash.history 
bleachbit:  /usr/bin/bleachbit

[config]
timeout:    90000 
title:      Clean system data
hide:       False
button:     icon.gif 
root:       True
assert:     %(bleachbit)s

[cmd]
check:      check.py 
start:      start.py
stop:
```
