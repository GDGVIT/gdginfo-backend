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


"""
@api {get} /leaderboard org leaderboard 
@apiName org leaderboard
@apiGroup all
@apiParamExample {json} response-example
{
    status: 200,
    message: "OK",
    payload: {
        L04DB4L4NC3R: 82,
        Angad Sharma: 16816,
        bhaveshgoyal27: 19,
        dependabot-preview[bot]: 3743,
        shashu421: 2150,
        HRITISHA: 1105,
        alan478: 8805,
        Krishn157: 930
    }
}
"""
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
        
"""
@api {get} /topcontributors top contributors of the org
@apiName top contributors of the org
@apiGroup all
@apiParamExample {json} response-example
{
    status: 200,
    message: "OK",
    payload: {
        CodeCombat: "Angad Sharma",
        skin-cancer-detection: "shashu421",
        cc-website-prototype-19: "HRITISHA",
        github-orgs-api: "Angad Sharma",
        digital-beacon: "Angad Sharma",
        vit-tourist-guide: "alan478",
        DevSoc2K19-Website: "Angad Sharma",
        love-open-source: "Angad Sharma",
        notes-map-analytics: "Angad Sharma",
        smart-park: "Angad Sharma",
        webinars: "L04DB4L4NC3R"
    }
}
"""
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

"""
@api {get} /repos data related to repos
@apiName data related to repos
@apiGroup all
@apiParamExample {json} response-example
{
    status: 200,
    message: "OK",
    payload: [
        {
            ref: {
                target: {
                    history: {
                        edges: [
                                    {
                                        node: {
                                            deletions: 1,
                                            additions: 1,
                                            author: {
                                                date: "2019-06-04T20:37:49+05:30",
                                                name: "Angad Sharma"
                                                }
                                        }
                                    }
                                ]
                            }
                    }
            },
            name: "github-orgs-api"
            }]
"""
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

"""
@api {get} /seed manually seed cache 
@apiName manually seed cache
@apiGroup all
"""
class ManualSeed(RequestHandler):
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
        utility.cache_response(self.token, self.org, self.redis)
        self.write("Cache seeded")
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
        utility.cache_response(token=token, org=org, rd=r) # seed cache
        cron.start_cache_job(token, org, r)
    else:
        r = None
   
    if token is None or org is None:
        print("Token or Organization was null")
        exit(1)
    
    # starting application
    application = Application([(r'/leaderboard', LeaderBoard, dict(redis=r, token=token, org=org)),
                           (r'/topcontributors', TopContributors, dict(redis=r, token=token, org=org)),
                           (r'/repos', Repos, dict(redis=r, token=token, org=org)),
                           (r'/seed', ManualSeed, dict(redis=r, token=token, org=org))
                           ], **settings)
    server = HTTPServer(application)
    server.listen(os.environ.get("PORT", 5000))
    IOLoop.current().start()
