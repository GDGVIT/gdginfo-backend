# Tornado libraries
from tornado.ioloop import IOLoop
from tornado.web import RequestHandler, Application, removeslash
from tornado.httpserver import HTTPServer
from tornado.gen import coroutine

# Other libraries
import json
import os
from bin import utility


class LeaderBoard(RequestHandler):
    
    def set_default_headers(self):
        print("setting headers!!!")
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header('Access-Control-Allow-Methods', 'GET, OPTIONS')

    @coroutine
    def get(self):
        res = utility.leaderboard()

        jsonData = {
            'status': 200,
            'message': 'OK',
            'payload': res
        }
        self.write(json.dumps(jsonData))
        
    def write_error(self, status_code, **kwargs):
        jsonData = {
            'status': int(status_code),
            'message': "Internal server error",
            'answer': 'NULL'
        }
        self.write(json.dumps(jsonData))

    def options(self):
        self.set_status(204)
        self.finish()
        

class TopContributors(RequestHandler):
    
    def set_default_headers(self):
        print("setting headers!!!")
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header('Access-Control-Allow-Methods', 'GET, OPTIONS')
    
    @coroutine
    def get(self):
        response = utility.topcontributor()

        jsonData = {
            'status' : 200,
            'message' : 'OK',
            'payload' : response
        
        }
        self.write(json.dumps(jsonData))
        
    def write_error(self, status_code, **kwargs):
        jsonData = {
            'status': int(status_code),
            'message': "Internal server error",
            'answer': 'NULL'
        }
        self.write(json.dumps(jsonData))
    def options(self):
        self.set_status(204)
        self.finish()


class Repos(RequestHandler):
    
    def set_default_headers(self):
        print("setting headers!!!")
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header('Access-Control-Allow-Methods', 'GET, OPTIONS')
    
    @coroutine
    def get(self):
        response = utility.extract_repos()

        jsonData = {
            'status' : 200,
            'message' : 'OK',
            'payload' : response
        
        }
        self.write(json.dumps(jsonData))
        
    def write_error(self, status_code, **kwargs):
        jsonData = {
            'status': int(status_code),
            'message': "Internal server error",
            'answer': 'NULL'
        }
        self.write(json.dumps(jsonData))
    def options(self):
        self.set_status(204)
        self.finish()


settings = dict(
    debug=True
)

application = Application([(r'/leaderboard', LeaderBoard),
                           (r'/topcontributors', TopContributors),
                           (r'/all', Repos)
                           ], **settings)

if __name__ == "__main__":
    server = HTTPServer(application)
    server.listen(os.environ.get("PORT", 5000))
    IOLoop.current().start()
