import simplejson as json
from tornado.gen import coroutine
from tornado.web import RequestHandler
from tornado_cors import CorsMixin

from utility import utility


"""
@api {get} /repos data related to repos
@apiName data related to repos
@apiGroup all
@apiParam org organization name
@apiPermission logged-in
@apiParamExample {json} response-example
{
    status: 200,
    message: "OK",
    payload:
        {
		"name": "CodeCombat",
		"ref": {
			"target": {
				"history": {
					"edges": [{
						"node": {
							"author": {
								"name": "Angad Sharma",
								"date": "2019-06-06T08:38:08+05:30"
							},
							"additions": 3,
							"deletions": 27,
							"pushedDate": "2019-06-06T03:08:09Z",
							"message": "Merge pull request #8 from CodeChefVIT/dependabot/npm_and_yarn/mongoose-5.5.13\n\nBump mongoose from 5.5.12 to 5.5.13",
							"messageBody": "\u2026se-5.5.13\n\nBump mongoose from 5.5.12 to 5.5.13",
							"url": "https://github.com/CodeChefVIT/CodeCombat/commit/60e45681c9baf8b02c2996ffc14442741f0c6fea"
						}
					}]

                        }
                }
            }
        }
"""


class Repos(CorsMixin, RequestHandler):
    CORS_ORIGIN = "*"
    CORS_HEADERS = 'Content-Type, Authorization'
    CORS_METHODS = 'GET'
    CORS_MAX_AGE = 21600
    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header('Access-Control-Allow-Methods', 'GET, OPTIONS')
        self.set_header('Access-Control-Allow-Headers', 'authorization')

    def initialize(self, redis):
        self.redis = redis

    @coroutine
    def get(self):
        token=self.request.headers.get("Authorization")
        if token is None or not token:
            self.write("You are not logged in")

        org=self.get_query_argument("org")
        response = utility.repos(token, org, self.redis)
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

