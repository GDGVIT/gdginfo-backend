import simplejson as json
from tornado_cors import CorsMixin
from tornado.gen import coroutine
from tornado.web import RequestHandler

from utility import orgs

"""
@api {get} /orgs get a list of organizations
@apiName get a list of organizations
@apiGroup all
@apiPermission logged-in
@apiParamExample {json} response-example
{
  "data": {
    "viewer": {
      "organizations": {
        "nodes": [
          {
            "name": "DSC VIT Vellore",
            "url": "https://github.com/GDGVIT",
            "login": "GDGVIT",
            "avatarUrl": "https://avatars0.githubusercontent.com/u/11557748?v=4",
            "websiteUrl": "https://dscvit.com/",
            "description": "Google Developers Group VIT"
          },
          {
            "name": "CodeChef - VIT Vellore",
            "url": "https://github.com/CodeChefVIT",
            "login": "CodeChefVIT",
            "avatarUrl": "https://avatars2.githubusercontent.com/u/31820857?v=4",
            "websiteUrl": "www.codechefvit.com",
            "description": "CodeChef is a technical chapter in VIT University Vellore that helps students all over the campus to improve their coding skills."
          }
        ]
      }
    }
  }
}
"""


class Orgs(CorsMixin, RequestHandler):
    CORS_ORIGIN = "*"
    CORS_HEADERS = 'Content-Type, Authorization'
    CORS_METHODS = 'GET'
    CORS_MAX_AGE = 21600

    @coroutine
    def get(self):
        token=self.request.headers.get("Authorization")
        if token is None or not token:
            self.write("You are not logged in")
            return
        res = orgs.get_orgs(token)
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

