# Tornado libraries
from tornado.ioloop import IOLoop
from tornado.web import RequestHandler, Application, removeslash
from tornado.httpserver import HTTPServer
from tornado.gen import coroutine

# Other libraries
import json
import os
import sys
import redis
from utility import utility, cron
from dotenv import load_dotenv



class LeaderBoard(RequestHandler):
    def initialize(self, redis, token, org):
        self.token = token
        self.org = org
        self.redis = redis

    def set_default_headers(self):
        print("setting headers!!!")
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header('Access-Control-Allow-Methods', 'GET, OPTIONS')

    @coroutine
    def get(self):
        res = utility.leaderboard(self.token, self.org, self.redis)

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
    def initialize(self, redis, token, org):
        self.token = token
        self.org = org
        self.redis = redis

    def set_default_headers(self):
        print("setting headers!!!")
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header('Access-Control-Allow-Methods', 'GET, OPTIONS')
    
    @coroutine
    def get(self):
        response = utility.topcontributor(self.token, self.org, self.redis)
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
    def initialize(self, redis, token, org):
        self.token = token
        self.org = org
        self.redis = redis
    def set_default_headers(self):
        print("setting headers!!!")
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header('Access-Control-Allow-Methods', 'GET, OPTIONS')
    @coroutine
    def get(self):
        response = utility.repos(self.token, self.org, self.redis)
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


if __name__ == "__main__":
    load_dotenv(dotenv_path="./.env", verbose=True)
    token = os.environ.get("TOKEN")
    org = os.environ.get("ORGANIZATION")
    if len(sys.argv) > 1 and sys.argv[1] == "--with-cache":
        print("Connecting to redis....")
        r = redis.from_url(os.environ.get("REDIS_URL"))
        if r is None:
            print("[ERROR] cannot connect to caching layer")
            exit(2)
        utility.cache_response(token, org, r) # seed cache
        cron.start_cache_job(token, org, r)
    else:
        r = None
   
    if token is None or org is None:
        print("Token or Organization was null")
        exit(1)
    
    # starting application
    application = Application([(r'/leaderboard', LeaderBoard, dict(redis=r, token=token, org=org)),
                           (r'/topcontributors', TopContributors, dict(redis=r, token=token, org=org)),
                           (r'/all', Repos, dict(redis=r, token=token, org=org))
                           ], **settings)
    server = HTTPServer(application)
    server.listen(os.environ.get("PORT", 5000))
    IOLoop.current().start()
