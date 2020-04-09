#!/usr/bin/env python3

import os
import sys
import redis
import simplejson as json

import tornado.gen
import tornado.httpclient
import tornado.ioloop
import tornado.web
from tornado.concurrent import return_future
from tornado.gen import coroutine
from tornado.web import RequestHandler

from dotenv import load_dotenv
from routes import leaderboard, oauth, repos, seed, orgs, analyze

load_dotenv(dotenv_path="./.env", verbose=True)
GITHUB_CLIENT_ID = os.environ.get("GITHUB_CLIENT_ID")
GITHUB_CLIENT_SECRET = os.environ.get("GITHUB_CLIENT_SECRET")


class Welcome(RequestHandler):
    def set_default_headers(self):
        print("setting headers!!!")
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header('Access-Control-Allow-Methods', 'GET, OPTIONS')

    @coroutine
    def get(self):
        self.write("Hello world")

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


def main():
    org = os.environ.get("ORGANIZATION")
    if len(sys.argv) > 1 and sys.argv[1] == "--with-cache":
        print("Connecting to redis....")
        r = redis.from_url(os.environ.get("REDIS_URL"))
        if r is None:
            print("[ERROR] cannot connect to caching layer")
            exit(2)
        # utility.cache_response(token=token, org=org, rd=r)  # seed cache
    else:
        r = None

    if org is None:
        print("Organization was null")
        exit(1)

    handlers = [
        (r"/token", oauth.GetToken),
        (r"/oauth", oauth.GithubLoginHandler),
        (r"/logout", oauth.LogoutHandler),
        ('/leaderboard', leaderboard.LeaderBoard, dict(redis=r)),
        (r'/topcontributors', leaderboard.TopContributors, dict(redis=r)),
        (r'/repos', repos.Repos, dict(redis=r)),
        (r'/seed', seed.ManualSeed, dict(redis=r)),
        (r'/orgs', orgs.Orgs),
        (r'/analyze', analyze.AnalyzeFmtHTML, dict(redis=r)),
        (r'/json/analyze', analyze.AnalyzeFmtJSON, dict(redis=r)),
        (r'/', Welcome)
    ]

    settings = dict(
        cookie_secret="asdf",
        login_url="/oauth",
        xsrf_cookies=True,
        github_client_id=GITHUB_CLIENT_ID,
        github_client_secret=GITHUB_CLIENT_SECRET,
        github_callback_path="/oauth",
        github_scope="read:repo, read:user, read:org",
        debug=True,
        autoescape=None,
        request_timeout=5.0,
        connect_timeout=5.0,
    )

    tornado.httpclient.AsyncHTTPClient.configure(
        "tornado.curl_httpclient.CurlAsyncHTTPClient")

    print("Listening....")
    application = tornado.web.Application(handlers, **settings)
    port = os.environ.get("PORT", 3000)
    print("Starting on port ", port)
    application.listen(port)
    tornado.ioloop.IOLoop().instance().start()


if __name__ == "__main__":
    main()
