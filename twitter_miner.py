import tweepy
from tweepy import OAuthHandler
import warnings
from html import HTML
import json

#suppress the potential warning message
warnings.filterwarnings("ignore")

def twitter_api_login(): #Login
	consumer_key = 'eOlWInbxWsb0GrFb7sPbcerfG'
	consumer_secret = 'vYAwYaGhgV2PSikjUyYZbUFheDDvckYlKl5ArYLdzlYSju8vYk'
	access_token = '716475678993072128-7kVKnlTYWw27l0SJefrUEGjtnAspi1B'
	access_secret = 'f7OAtB4sCp24ABvBxTaMRqCuR8iMMTeLO4QzscwGNZ6J3'
 	#access_secret = 'f7OAtB4sCp24ABvBxTaMRqCuR8iMMTeLO4QzscwGNZ6J4'
	auth = OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_token, access_secret)
 
	api = tweepy.API(auth)
	return api

def format_status(status): 
	"""
	convert each raw status into the required html-like format
	"""
	entities_list= []
	entity_type_list = ["user_mentions", "hashtags","urls"] #the three most popular entity types
	if "media" in status.entities: #add media into entity_type_list if it appears in this status
		entity_type_list.append("media")
	
	for entity_type in entity_type_list:
		for entity in  status.entities[entity_type]:
			entity.update({"entity_type":entity_type})
			entities_list.append(dict(entity))
	if len(entities_list)!= 0:
		entities_list.sort(key= lambda item:item["indices"][0], reverse= True)
	#convert status into required html-like format according to different entity type	
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
	"""
	get the list of statuses as requested and the next_cursor/min_id
	"""
	statuses_list = []
	
	for user_name in users:
	    try:
		for status in tweepy.Cursor(api.user_timeline, screen_name=user_name, max_id =  (max_id - 1 if max_id else None)  ).items(count):
			statuses_list.append(status)
	    except Exception as e:
		#when failing to get statuses from user, print the error message
		error_dict = json.loads(e.message)
		for error_message in error_dict["errors"]:
			print "Error Message occurs when trying to get statuses from user %s : %s" % (user_name, error_message["message"])
	#get the count number of most recent statuses from users that are before max_id
	statuses_list.sort(key = lambda x: x.id, reverse = True) 
	top_statuses_list = statuses_list[0:count]
	#get the minimum id/next cursor
	if len(top_statuses_list) != 0:
		min_id = min([status.id for status in top_statuses_list])
	else:
		min_id = max_id
	return top_statuses_list, min_id

def construct_json(statuses_list, next_cursor):
	"""
	convert statuses list and next_cursor into a dictionary which is consistent with the desired json format
	"""
	json_dict = {}
	json_dict["next_cursor"] = str(next_cursor)
	json_dict["statuses"] = []
	
	for status in statuses_list:
		
		json_dict["statuses"].append({"status":format_status(status), "user":status.user.screen_name})

	return json_dict

def twitter_miner(users, count, cursor):
	"""
	This is the main function of twitter miner
	"""
	#login to the twitter api
	api=twitter_api_login()
	#get the list of statuses and next_cursor
	status, next_cursor = get_statuses(api, users, count, cursor)
	#convert the statuses and next_cursor into json_dict of dictionary format which is consistent with the desired json format
	json_dict = construct_json(status, next_cursor)
	#convert the json_dict into json_result which is of json type 
	json_result = json.dumps(json_dict)
	return json_result

def write2html(json_result, outputfile_name):
	"""
	convert json result into html file
	"""
	result = json.loads(json_result)
	
	f= open(outputfile_name,'w')
	for status_index in range(len(result["statuses"])):
		status = result["statuses"][status_index]["status"]
		f.write(status.encode("utf8"))
		f.write("\n")
	f.close()


def test_case(): 
	#test function for this file
        users = ["BigSeannihao", "forestliurui"]
        #users = ["forestliurui"]
	count = 5
	cursor = None
        result = twitter_miner(users, count, cursor)
	outputfile_name = "test_miner.html"
	write2html(result, outputfile_name)
	import pdb;pdb.set_trace()

if __name__ == "__main__":
	#invoke test function when this script is run from command line
	test_case()




