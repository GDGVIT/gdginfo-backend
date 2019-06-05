from tornado.web import RequestHandler
from tornado.gen import coroutine

import simplejson as json
from utility import utility
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


