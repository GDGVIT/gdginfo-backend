import simplejson as json
from tornado.gen import coroutine
from tornado.web import RequestHandler

from utility import utility


"""
@api {get} /seed manually seed cache
@apiName manually seed cache
@apiPermission logged-in
@apiGroup all
"""
class ManualSeed(RequestHandler):
    def initialize(self, redis, org):
        self.org = org
        self.redis = redis

    def set_default_headers(self):
        print("setting headers!!!")
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header('Access-Control-Allow-Methods', 'GET, OPTIONS')

    @coroutine
    def get(self):
        user = self.get_secure_cookie("user")
        if user is None or not user:
            self.write("You are not logged in")
            return
        data = json.loads(user)
        token = data["access_token"]

        utility.cache_response(token, self.org, self.redis)
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
