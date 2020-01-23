import simplejson as json
from tornado.gen import coroutine
from tornado.web import RequestHandler

from utility import analyze


class Analyze(RequestHandler):
    def initialize(self, redis, org):
        self.org=org
        self.redis = redis

    def set_default_headers(self):
        print("setting headers!!!")
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header('Access-Control-Allow-Methods', 'GET, OPTIONS')

    @coroutine
    def get(self, slug=None):
        # user = self.get_secure_cookie("user")
        # if user is None or not user:
            # self.write("You are not logged in")
            # return


        data, err = analyze.analyze(slug, self.org, self.redis)
        jsonData = {
             'status': 200,
             'message': 'OK',                
             'error': err,
             'payload': data
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
