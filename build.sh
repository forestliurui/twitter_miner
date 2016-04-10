#!/bin/bash
#This is the bash script to install any needed dependencies for twitter miner

#I use python 2.7.6 (default python for ubuntu) for the entire program. Please make sure the same version of python is installed 

#pip is ued to install the required python packages
#install pip first
sudo apt-get install python-pip

sudo pip install tweepy==3.3.0
sudo pip install html
sudo pip install cherrypy
sudo pip install requests



