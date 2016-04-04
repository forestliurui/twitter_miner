import random
import string
from twitter_miner import twitter_miner
import cherrypy

class StringGeneratorWebService(object):
     exposed = True

     @cherrypy.tools.accept(media='text/plain')
     def GET(self, screen_names =None, count = None, cursor = None):
	 
         screen_names = screen_names.split(",")
	 count = int(count)
         if cursor is not None:
		cursor = int(cursor) 	
	 json_result = twitter_miner(screen_names, count, cursor)
	 #import pdb;pdb.set_trace()
         return json_result

     def POST(self, length=8):
         some_string = ''.join(random.sample(string.hexdigits, int(length)))
         cherrypy.session['mystring'] = some_string
         return some_string

     def PUT(self, another_string):
         cherrypy.session['mystring'] = another_string

     def DELETE(self):
         cherrypy.session.pop('mystring', None)

if __name__ == '__main__':
     Port = 80
     conf = {
         '/': {
             'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
             'tools.sessions.on': True,
             'tools.response_headers.on': True,
             'tools.response_headers.headers': [('Content-Type', 'text/plain')],
         }
     }

     cherrypy.quickstart(StringGeneratorWebService(), '/', conf)
