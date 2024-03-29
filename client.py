"""
This is the client of twitter miner which will communicate with server program to extract desired information
"""

import requests
import json
from urllib import urlencode
from twitter_miner import write2html


def client(screen_names, count):
	#open an session with server program
	s = requests.Session()
	
	params ={"screen_names": ",".join(screen_names), "count": count}
	
	url =  "http://localhost:8080?"
	url += urlencode(params)   #get the complete URL
	#url will look like "http://localhost:8080?screen_names=user1,user2&count=5"
	
	r = s.get(url) #Send GET request
	json_return = r.text #extract requested json-type result
	
	#write the json-type result into an html file
	write2html(json_return, "test1.html")
	


	#the following code tries to use the returned next_cursor to send another request
	json_object = json.loads(json_return)
	
	url +="&cursor="+json_object["next_cursor"]
	r = s.get(url) #Send another GET request with cursor set as next_cursor from previous request
        json_return = r.text
        json_object = json.loads(json_return)
	write2html(json_return, "test2.html")
	

if __name__ == "__main__":
	#specify the screen names and count
	screen_names =  ["kobebryant", "StephenCurry30"]
        count = 5
	client(screen_names, count)
