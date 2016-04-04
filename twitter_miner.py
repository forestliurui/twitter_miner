import tweepy
from tweepy import OAuthHandler
import warnings
from html import HTML
import json

warnings.filterwarnings("ignore")

def twitter_api_login():
	consumer_key = 'eOlWInbxWsb0GrFb7sPbcerfG'
	consumer_secret = 'vYAwYaGhgV2PSikjUyYZbUFheDDvckYlKl5ArYLdzlYSju8vYk'
	access_token = '716475678993072128-7kVKnlTYWw27l0SJefrUEGjtnAspi1B'
	access_secret = 'f7OAtB4sCp24ABvBxTaMRqCuR8iMMTeLO4QzscwGNZ6J3'
 
	auth = OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_token, access_secret)
 
	api = tweepy.API(auth)
	return api

def format_status(status):
	#h = HTML(newlines = False)
	#import pdb;pdb.set_trace()
	entities_list= []
	entity_type_list = ["user_mentions", "hashtags","urls"]
	if "media" in status.entities:
		entity_type_list.append("media")
	for entity_type in entity_type_list:
		for entity in  status.entities[entity_type]:
			entity.update({"entity_type":entity_type})
			entities_list.append(dict(entity))
	if len(entities_list)!= 0:
		entities_list.sort(key= lambda item:item["indices"][0], reverse= True)
	#import pdb;pdb.set_trace()
	status_formated = status.text
	for entity in entities_list:
		if entity["entity_type"] == "user_mentions":
			h = HTML()
			h.a(status_formated[int(entity["indices"][0]): entity["indices"][1]], href ="https://twitter.com/"+entity["screen_name"])
		elif entity["entity_type"] == "hashtags":
			h = HTML()
			h.a(status_formated[int(entity["indices"][0]): int(entity["indices"][1])], href = "https://twitter.com/hashtag/"+entity["text"])
		else:
			h = HTML()
			h.a(entity["display_url"], href = entity["expanded_url"])
		status_formated = status_formated[0:int(entity["indices"][0])]+unicode(h)+status_formated[int(entity["indices"][1]):]
	return status_formated


def get_statuses(api, users, count, max_id = None):
	statuses_list = []
	for user_name in users:
		for status in tweepy.Cursor(api.user_timeline, screen_name=user_name, max_id =  (max_id - 1 if max_id else None)  ).items(count):
			statuses_list.append(status)
	statuses_list.sort(key = lambda x: x.id, reverse = True)
	top_statuses_list = statuses_list[0:count]
	if len(top_statuses_list) != 0:
		min_id = min([status.id for status in top_statuses_list])
	else:
		min_id = max_id
	return top_statuses_list, min_id

def construct_json(statuses_list, next_cursor):
	json_dict = {}
	json_dict["next_cursor"] = str(next_cursor)
	json_dict["statuses"] = []
	
	for status in statuses_list:
		
		json_dict["statuses"].append({"status":format_status(status), "user":status.user.screen_name})

	return json_dict

def twitter_miner(users, count, cursor):


	api=twitter_api_login()

	#count = 5
	#users=["forestliurui", "joebonsall", "TheDeenShow"]
	#users = ["forestliurui"]
	

	
	status, min_id = get_statuses(api, users, count, cursor)
	#import pdb;pdb.set_trace()
	json_dict = construct_json(status, min_id)
	json_result = json.dumps(json_dict)
	return json_result

def test_case():
        users = ["BigSean"]
        count = 5
	cursor = None
        result = twitter_miner(users, count, cursor)
	import pdb;pdb.set_trace()

if __name__ == "__main__":
	test_case()

"""
status2, min_id = get_statuses(api, users, count, min_id)
json_dict2 = construct_json(status2, min_id)

num = 1
for status in status1:
	print(str(num)+": ")
        print(status.text)
        print(format_status(status)) 
	num += 1
for status in status2:
        print(str(num)+": ")
        print(status.text)
        print(format_status(status))
        num += 1


import pdb;pdb.set_trace()

num = 1
min_id = None
for status in tweepy.Cursor(api.user_timeline, screen_name="joebonsall").items(10):
    # Process a single status
    	print(str(num)+": ")
	print(status.text)
	print(format_status(status))
	#import pdb;pdb.set_trace()
	#print(status.next_cursor)
	if min_id is None:
		min_id = status.id
	else:
		min_id = min(min_id, status.id)
	num+=1 

for status in tweepy.Cursor(api.user_timeline, screen_name="joebonsall", max_id = min_id -1  ).items(4):
    # Process a single status
        print(str(num)+": ")
        print(status.text)
        #import pdb;pdb.set_trace()
        #print(status.next_cursor)
        if min_id is None:
                min_id = status.id
        else:
                min_id = min(min_id, status.id)
        num+=1
"""




