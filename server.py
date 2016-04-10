"""
This is the server of twitter miner implemented using cherrypy
"""

import random
import string
from twitter_miner import twitter_miner
import cherrypy

class Miner_Server(object):
     	exposed = True

     	@cherrypy.tools.accept(media='text/plain')
	def GET(self, screen_names =None, count = None, cursor = None):
	 
        	screen_names = screen_names.split(",")
		count = int(count)
        	if cursor is not None:
			cursor = int(cursor) 	
		#invoke the twitter miner to get the json-type result 
		json_result = twitter_miner(screen_names, count, cursor)
	 
		return json_result
  
if __name__ == '__main__':
     	
     	#configuration of server	
     	conf = {
         '/': {
             	'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
             	'tools.sessions.on': True,
             	'tools.response_headers.on': True,
             	'tools.response_headers.headers': [('Content-Type', 'text/plain')],
             	'port':8000,
		}
	}
  
	cherrypy.quickstart(Miner_Server(), '/', conf) 
     

     
