import requests
import json

def client():
	s = requests.Session()
	url = "http://localhost:8080?screen_names=forestliurui,TheDeenShow&count=3"
	r = s.get(url)
	json_return = r.text
	json_object = json.loads(json_return)
	print json_object
	url +="&cursor="+json_object["next_cursor"]
	r = s.get(url)
        json_return = r.text
        json_object = json.loads(json_return)
	print json_object
	import pdb;pdb.set_trace()	

if __name__ == "__main__":
	client()
