#!/bin/bash

#this script will invoke the server and client to test the twitter miner

echo "starting server"
python server.py &
#sleep for 5 seconds so that server can finish initialization before we run client
sleep 5
echo "starting client"
python client.py
