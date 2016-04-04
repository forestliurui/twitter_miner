import requests
import json
from urllib import urlencode

def client():
	s = requests.Session()
	screen_names = ["forestliurui", "TheDeenShow", "BigSean"]
	count = 5
	params ={"screen_names": ",".join(screen_names), "count": count}
	
	url =  "http://localhost:8080?"
	url += urlencode(params)

	#url = "http://localhost:8080?screen_names=forestliurui,TheDeenShow&count=3"
	r = s.get(url)
	json_return = r.text
	json_object = json.loads(json_return)
	print json_object
	print ""
	url +="&cursor="+json_object["next_cursor"]
	r = s.get(url)
        json_return = r.text
        json_object = json.loads(json_return)
	print json_object
	import pdb;pdb.set_trace()	

if __name__ == "__main__":
	client()
