import simplejson as json
from tornado.gen import coroutine
from tornado.web import RequestHandler

from utility import utility


"""
@api {get} /repos data related to repos
@apiName data related to repos
@apiGroup all
@apiPermission logged-in
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
            self.redirect("/oauth")
        data = json.loads(user)
        token = data["access_token"]
        response = utility.repos(token, self.org, self.redis)
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
