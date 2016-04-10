Twitter Miner
=============

Overview
--------

This Twitter Miner contains the program to extract required number of most recent statuses of pre-specified twitter users. It's written in Python.  

Installation
------------

Please run build.sh to install relevant packages/libraries:
    
     ./build.sh

Usage
-----

To use the Twitter Miner, simply run the script run.sh after installation of relevant packages:

     ./run.sh

It will first execute the server.py and let it running in the background. Then, after 5-second sleep (server needs some time to initialize), client.py will be executed which will tries to request statues using GET method.

Contents
--------

There are three source files: twitter_miner.py, server.py and client.py

twitter_miner.py contains the main parts of required functionality. It is responsible for extracting required number of most recent statuses of pre-specified twitter users and returning the results in required json format.

server.py makes use of package cherrypy to build a server which could receive requests and then invoke functions in twitter_miner.py to get requested statuses

client.py can build connection with server and send desired GET request to server. It will send two consecutive requests. The first one is without cursor.
The second request is with cursor field, which is set to be the next_cursor from first response. Both of responses are written into html files so that we can check if the program is running as desired.   

Note: if non-existed screen name or wrong authentication is provided, error handling code in twitter_miner.py will take care of it and print error messages to stdout.

 




