import requests
import json
from urllib import urlencode
from twitter_miner import write2html

def client():
	s = requests.Session()
	screen_names = ["forestliurui", "BigSean"]
	count = 5
	params ={"screen_names": ",".join(screen_names), "count": count}
	
	url =  "http://localhost:8080?"
	url += urlencode(params)


	#url = "http://localhost:8080?screen_names=forestliurui,TheDeenShow&count=3"
	r = s.get(url)
	json_return = r.text
	
	write2html(json_return, "test1.html")
	
	json_object = json.loads(json_return)
	"""
	print json_object
	print ""
	
	file_name = "123.html"
	with open(file_name, "a+") as fp:
		for status in json_object["statuses"]:
			#fp.write(status["status"])
			json.dump(status["status"],fp)
	"""
	url +="&cursor="+json_object["next_cursor"]
	r = s.get(url)
        json_return = r.text
        json_object = json.loads(json_return)
	write2html(json_return, "test2.html")
	#print json_object
	#import pdb;pdb.set_trace()	

if __name__ == "__main__":
	client()
