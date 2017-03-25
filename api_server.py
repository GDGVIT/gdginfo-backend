import tornado.ioloop
import tornado.web
from tornado.httpserver import HTTPServer
import tornado.options
from pymongo import MongoClient
from tornado.gen import coroutine

import json

db=MongoClient("mongodb://apuayush:qwerty1234@ds137110.mlab.com:37110/githubleaderboard")['githubleaderboard']
#db = MongoClient("localhost", 27017)['githubleaderboard']
coll1=db['score']
coll2=db['top']

from tornado.options import define,options
define("port",default=7777,help="run on the given port",type=int)


class ApiHandler(tornado.web.RequestHandler):
    @coroutine
    @tornado.web.removeslash
    def get(self):
        response =[]
        for members in db.coll1.find():
            #response.append(members['login'])
            k=members
            k.pop('_id')
            response.append(k)

        self.write(json.dumps(response))

class TopContributors(tornado.web.RequestHandler):
    def get(self):
        response=[]
        for top_con in db.coll2.find():
            k=top_con
            k.pop('_id')
            response.append(k)
        self.write(json.dumps(response))



if __name__ == "__main__":
    tornado.options.parse_command_line()
    app = tornado.web.Application(handlers=[(r'/leaderboard', ApiHandler),(r'/topcontributors',TopContributors)], db=db,
                                  debug=True)
    server = HTTPServer(app)
    server.listen(options.port)
    tornado.ioloop.IOLoop.current().start()
