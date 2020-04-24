import simplejson as json
from tornado.gen import coroutine
from tornado.web import RequestHandler
from tornado_cors import CorsMixin

from utility import utility


"""
@api {get} /leaderboard org leaderboard
@apiName org leaderboard
@apiGroup all
@apiParam org organization name
@apiPermission logged-in
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
class LeaderBoard(CorsMixin, RequestHandler):
    CORS_ORIGIN = "*"
    CORS_HEADERS = 'Content-Type, Authorization'
    CORS_METHODS = 'GET'
    CORS_MAX_AGE = 21600
    def initialize(self, redis):
        self.redis = redis

    @coroutine
    def get(self):
        token=self.request.headers.get("authorization")
        if token is None or not token:
            self.write("You are not logged in")
            return

        org=self.get_query_argument("org")
        res = utility.leaderboard(token, org, self.redis)

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
@apiParam org organization name
@apiPermission logged-in
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

class TopContributors(CorsMixin, RequestHandler):
    CORS_ORIGIN = "*"
    CORS_HEADERS = 'Content-Type, Authorization'
    CORS_METHODS = 'GET'
    CORS_MAX_AGE = 21600
    def initialize(self, redis):
        self.redis = redis

    def get(self):
        token=self.request.headers.get("Authorization")
        if token is None or not token:
            self.write("You are not logged in")
            return

        org=self.get_query_argument("org")
        response = utility.topcontributor(token, org, self.redis)
        jsonData = {
            'status': 200,
            'message': 'OK',
            'payload': response

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

