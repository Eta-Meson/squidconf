#! /usr/bin/python
name = "K.Mohan Sai Krishna"

import os
import sys
import subprocess
import getpass
import apt

filename = "squid.conf"

#initializs the chain
def start():
	installcheck();
	return

# Check if the squid is already installed.
def installcheck():
	if os.path.isdir("/etc/squid3/") == True:
		print("squid directory exists")
		backup();
	else:
		print("Seems squid is not installed. Going to install squid")
		installsquid();
	return


# Install squid if not installed.
def installsquid():
	subprocess.call(["sudo","-E","apt-get","install","squid"])
	backup();
	return


# Backup the curent squid.conf file
def backup():
	if os.path.isfile("/etc/squid3/squid.conf") == True:		
		print("Backing up your squid.conf file")
		print("Renaming it as squid.conf.original")
		subprocess.call(["sudo","mv","/etc/squid3/squid.conf","/etc/squid3/squid.conf.original"])
		check();
	elif os.path.isfile("/etc/squid3/squid.conf") == False:
		check();
	return
# Check if squid.conf exists incase the user runs this twice.	
def check():
	if os.path.isfile("/etc/squid3/squid.conf") == True:
		subprocess.call(["sudo","rm","/etc/squid3/squid.conf"])
	conf();
	return


# Main work happens here
def conf():
	port = raw_input('Enter the port to run your squid:')
	par_proxy = raw_input('Enter your parent proxy address:')
	par_port = raw_input('Enter your parent proxy port:')
	user = raw_input('Enter your parent proxy user name:')
	while 1:
		passw1 = getpass.getpass('Enter your parent proxy password:')
		passw2 = getpass.getpass('Enter proxy password again:')
		if (passw1 == passw2):
			break
		else:
			print("Passwords didnot match. Please enter them again")
	file = open(filename,'a')
	file.write("http_port " + port +"\n")
	file.write("cache_peer "+par_proxy+" parent "+par_port+" 0 login="+user+":"+passw1+"\n")
	file.write("never_direct allow all"+"\n")
	file.write("http_access allow all")
	file.close()
	print("File saved !! now moving")
	print("removing old file if exists")
	subprocess.call(["sudo","rm","-f","/etc/squid3/squid.conf"])
	subprocess.call(["sudo","mv","squid.conf","/etc/squid3/squid.conf"])
	print("Succesfully configured !! yay")
	return


start();


# cache = apt.Cache()
# cache.open()
# cache["squid"].is_installed	# Evaluates true if squid is installed