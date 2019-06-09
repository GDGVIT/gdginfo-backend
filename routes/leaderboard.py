import simplejson as json
from tornado.gen import coroutine
from tornado.web import RequestHandler

from utility import utility


"""
@api {get} /leaderboard org leaderboard
@apiName org leaderboard
@apiGroup all
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


class LeaderBoard(RequestHandler):
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
        res = utility.leaderboard(token, self.org, self.redis)

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


class TopContributors(RequestHandler):
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

        response = utility.topcontributor(token, self.org, self.redis)
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
