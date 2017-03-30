# Tornado libraries
from tornado.ioloop import IOLoop
from tornado.web import RequestHandler, Application, asynchronous, removeslash
from tornado.httpserver import HTTPServer
from tornado.httpclient import AsyncHTTPClient
from tornado.gen import engine, Task, coroutine, Return

# Other libraries
import json
import os
from motor import MotorClient

db = MotorClient(os.environ['DB_LINK'])['githubleaderboard']
coll1 = db['score']
coll2 = db['top']

class ApiHandler(RequestHandler):
    
    def set_default_headers(self):
        print "setting headers!!!"
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header('Access-Control-Allow-Methods', 'GET, OPTIONS')
    
    @coroutine
    @removeslash
    def get(self):
        response = {}
        members = db.coll1.find()

        while(yield members.fetch_next):
            member = members.next_object()
            response[member['username']] = member['score']

        jsonData = {
        'status' : 200,
        'message' : 'OK',
        'payload' : response
        
        
        }
        self.write(json.dumps(jsonData))
        
    def write_error(self,status_code,**kwargs):
        jsonData = {
        'status' : int(status_code),
        'message' : "Internal server error",
        'answer' : 'NULL'
        }
        self.write(json.dumps(jsonData))
    def options(self):
        self.set_status(204)
        self.finish()
        


class TopContributors(RequestHandler):
    
    def set_default_headers(self):
        print "setting headers!!!"
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header('Access-Control-Allow-Methods', 'GET, OPTIONS')
    
    @coroutine
    def get(self):
        response = {}
        top_contributors = db.coll2.find()

        while(yield top_contributors.fetch_next):
            contributor = top_contributors.next_object()
            response[contributor['repo']] = contributor['top']

        jsonData = {
        'status' : 200,
        'message' : 'OK',
        'payload' : response
        
        }
        self.write(json.dumps(jsonData))
        
    def write_error(self,status_code,**kwargs):
        jsonData = {
        'status' : int(status_code),
        'message' : "Internal server error",
        'answer' : 'NULL'
        }
        self.write(json.dumps(jsonData))
    def options(self):
        self.set_status(204)
        self.finish()


settings = dict(
    db=db,
    debug=True
)

application = Application([(r'/leaderboard', ApiHandler),
                           (r'/topcontributors', TopContributors),
                           ], **settings)

if __name__ == "__main__":
    server = HTTPServer(application)
    server.listen(os.environ.get("PORT",5000))
    IOLoop.current().start()
