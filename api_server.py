# Tornado libraries
from tornado.ioloop import IOLoop
from tornado.web import RequestHandler, Application, asynchronous, removeslash
from tornado.httpserver import HTTPServer
from tornado.httpclient import AsyncHTTPClient
from tornado.gen import engine, Task, coroutine, Return

# Other libraries
import json
import env

db = env.MOTOR_CLIENT
coll1 = db['score']
coll2 = db['top']

class ApiHandler(RequestHandler):
    @coroutine
    @removeslash
    def get(self):
        response = {}
        members = db.coll1.find()

        while(yield members.fetch_next):
            member = members.next_object()
            response[member['username']] = member['score']

        self.write(json.dumps(response))


class TopContributors(RequestHandler):
    @coroutine
    def get(self):
        response = {}
        top_contributors = db.coll2.find()

        while(yield top_contributors.fetch_next):
            contributor = top_contributors.next_object()
            response[contributor['repo']] = contributor['top']

        self.write(json.dumps(response))

settings = dict(
    db=db,
    debug=True
)

application = Application([(r'/leaderboard', ApiHandler),
                           (r'/topcontributors', TopContributors)
                           ], **settings)

if __name__ == "__main__":
    server = HTTPServer(application)
    server.listen(5000)
    IOLoop.current().start()
