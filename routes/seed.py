import simplejson as json
from tornado_cors import CorsMixin
from tornado.gen import coroutine
from tornado.web import RequestHandler

from utility import cron, utility


"""
@api {get} /seed manually seed cache [Hit only once]
@apiName manually seed cache
@apiParam org organization name
@apiPermission logged-in
@apiGroup all
"""
class ManualSeed(CorsMixin, RequestHandler):
    CORS_ORIGIN = "*"
    CORS_HEADERS = 'Content-Type, Authorization'
    CORS_METHODS = 'GET'
    CORS_MAX_AGE = 21600
    def initialize(self, redis):
        self.redis = redis

    def set_default_headers(self):
        print("setting headers!!!")
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header('Access-Control-Allow-Methods', 'GET, OPTIONS')

    @coroutine
    def get(self):
        token=self.request.headers.get("Authorization")
        if token is None or not token:
            self.write("You are not logged in")
            return

        org=self.get_query_argument("org")
        utility.cache_response(token, org, self.redis)

        # start CRON Job
        cron.start_cache_job(token, org, self.redis)
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

