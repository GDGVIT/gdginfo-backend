import simplejson as json
from tornado.gen import coroutine
from tornado.web import RequestHandler
from tornado_cors import CorsMixin

from utility import analyze


"""
@api {get} /analyze analyze a repository
@apiName analyze a repository
@apiParam org organization name
@apiParam repo repository name for the organization
@apiGroup all
@apiPermission logged-in
"""
class AnalyzeFmtHTML(CorsMixin, RequestHandler):
    CORS_ORIGIN = 'https://gdashboard.netlify.com'
    CORS_HEADERS = 'Content-Type'
    CORS_METHODS = 'POST'
    CORS_CREDENTIALS = True
    CORS_MAX_AGE = 21600

    def initialize(self, redis):
        self.redis = redis

    def set_default_headers(self):
        print("setting headers!!!")
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header('Access-Control-Allow-Methods', 'GET, OPTIONS')

    @coroutine
    def get(self, slug=None):
        user = self.get_secure_cookie("user")
        if user is None or not user:
            self.write("You are not logged in")
            return

        user=json.loads(user)
        token=user["access_token"]
        org=self.get_query_argument("org")
        repo=self.get_query_argument("repo")
        data, err = analyze.analyze(repo, org, self.redis, token, "html")
        if err is None:
            self.write(data)
            return
        self.write("<h1> Error occurred </h1> <br> <p> " + err + "</p> <br> <strong> " +
                "Trace: </strong> " + str(data))

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
@api {get} /json/analyze analyze a repository and spit out JSON
@apiName analyze a repository and spit out JSON
@apiGroup all
@apiParam org organization name
@apiParam repo repository name for the organization
@apiPermission logged-in
@apiParamExample {json} response-example
{
	"gitinspector": {
		"version": {
			"$": "0.4.4"
		},
		"repository": {
			"$": "GDGVIT_template"
		},
		"report-date": {
			"$": "2020/01/27"
		},
		"changes": {
			"message": {
				"$": "The following historical commit information, by author, was found in the repository"
			},
			"authors": {
				"author": [{
						"name": {
							"$": "Angad Sharma"
						},
						"gravatar": {
							"$": "https://www.gravatar.com/avatar/5e8def242c2dd4eede4822fe2f8944b4?default=identicon"
						},
						"commits": {
							"$": 1
						},
						"insertions": {
							"$": 1
						},
						"deletions": {
							"$": 0
						},
						"percentage-of-changes": {
							"$": 1.82
						}
					},
					{
						"name": {
							"$": "L04DB4L4NC3R"
						},
						"gravatar": {
							"$": "https://www.gravatar.com/avatar/5053cc8b4421a2e1f55a238b00430ace?default=identicon"
						},
						"commits": {
							"$": 1
						},
						"insertions": {
							"$": 53
						},
						"deletions": {
							"$": 1
						},
						"percentage-of-changes": {
							"$": 98.18
						}
					}
				]
			}
		},
		"blame": {
			"message": {
				"$": "Below are the number of rows from each author that have survived and are still intact in the current revision"
			},
			"authors": {
				"author": {
					"name": {
						"$": "L04DB4L4NC3R"
					},
					"gravatar": {
						"$": "https://www.gravatar.com/avatar/5053cc8b4421a2e1f55a238b00430ace?default=identicon"
					},
					"rows": {
						"$": 53
					},
					"stability": {
						"$": 100.0
					},
					"age": {
						"$": 0.0
					},
					"percentage-in-comments": {
						"$": 0.0
					}
				}
			}
		},
		"timeline": {
			"message": {
				"$": "The following history timeline has been gathered from the repository"
			},
			"periods": {
				"@length": "week",
				"period": {
					"name": {
						"$": "2020W03"
					},
					"authors": {
						"author": [{
								"name": {
									"$": "Angad Sharma"
								},
								"gravatar": {
									"$": "https://www.gravatar.com/avatar/5e8def242c2dd4eede4822fe2f8944b4?default=identicon"
								},
								"work": {
									"$": "."
								}
							},
							{
								"name": {
									"$": "L04DB4L4NC3R"
								},
								"gravatar": {
									"$": "https://www.gravatar.com/avatar/5053cc8b4421a2e1f55a238b00430ace?default=identicon"
								},
								"work": {
									"$": "+++++++++++++++++++++++"
								}
							}
						]
					},
					"modified_rows": {
						"$": 55
					}
				}
			}
		},
		"metrics": {
			"message": {
				"$": "No metrics violations were found in the repository"
			}
		},
		"responsibilities": {
			"message": {
				"$": "The following responsibilities, by author, were found in the current revision of the repository (comments are excluded from the line count, if possible)"
			},
			"authors": {
				"author": {
					"name": {
						"$": "L04DB4L4NC3R"
					},
					"gravatar": {
						"$": "https://www.gravatar.com/avatar/5053cc8b4421a2e1f55a238b00430ace?default=identicon"
					},
					"files": {
						"file": {
							"name": {
								"$": "README.md"
							},
							"rows": {
								"$": 53
							}
						}
					}
				}
			}
		},
		"extensions": {
			"message": {
				"$": "The extensions below were found in the repository history"
			},
			"used": {
				"extension": {
					"$": "md"
				}
			},
			"unused": {}
		}
	}
}
"""
class AnalyzeFmtJSON(CorsMixin, RequestHandler):
    CORS_ORIGIN = 'https://gdashboard.netlify.com'
    CORS_HEADERS = 'Content-Type'
    CORS_METHODS = 'POST'
    CORS_CREDENTIALS = True
    CORS_MAX_AGE = 21600
    def initialize(self, redis):
        self.redis = redis

    def set_default_headers(self):
        print("setting headers!!!")
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header('Access-Control-Allow-Methods', 'GET, OPTIONS')

    @coroutine
    def get(self, slug=None):
        user = self.get_secure_cookie("user")
        if user is None or not user:
            self.write("You are not logged in")
            return


        user=json.loads(user)
        token=user["access_token"]
        org=self.get_query_argument("org")
        repo=self.get_query_argument("repo")
        data, err = analyze.analyze(repo, org, self.redis, token, "xml")
        if err is None:
            self.write(data)
            return
        self.write("<h1> Error occurred </h1> <br> <p> " + err + "</p> <br> <strong> " +
                "Trace: </strong> " + str(data))

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

