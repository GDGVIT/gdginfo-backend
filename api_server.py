import tornado.ioloop
import tornado.web
from tornado.httpserver import HTTPServer
import tornado.options
from pymongo import MongoClient
from tornado.gen import coroutine
from tornado.options import define, options
import json



db = MongoClient("mongodb://apuayush:qwerty1234@ds137110.mlab.com:37110/githubleaderboard")['githubleaderboard']

#coll1 stores the score of all the members & coll2 stores the top contributors of all repos
coll1 = db['score']
coll2 = db['top']


define("port", default=7777, help="run on the given port", type=int)


class ApiHandler(tornado.web.RequestHandler):
    """This class returns a json response which has score of each member of an organization.
    this works on coll1 of db. Invokes when /leaderboard is called."""
    @coroutine
    @tornado.web.removeslash
    def get(self):
        response = []                   # response = the data taken from the coll1 of database with removed  _id value of the database
        for members in db.coll1.find(): # scrolling through coll1
            k = members
            k.pop('_id')                # remove the _id and append each member of coll to response
            response.append(k)

        self.write(json.dumps(response)) # converting response to a json and returning it


class TopContributors(tornado.web.RequestHandler):
    """This class returns a json response which has top contributors of each repository.
     this works on coll2 of db. Invokes when /topcontributors is called."""
    def get(self):
        response = []           # all same method as in class ApiHandler
        for top_con in db.coll2.find():
            k = top_con
            k.pop('_id')
            response.append(k)
        self.write(json.dumps(response))


if __name__ == "__main__":
    tornado.options.parse_command_line()
    app = tornado.web.Application(handlers=[(r'/leaderboard', ApiHandler), (r'/topcontributors', TopContributors)],
                                  db=db,
                                  debug=True)
    server = HTTPServer(app)
    server.listen(options.port)
    tornado.ioloop.IOLoop.current().start()
