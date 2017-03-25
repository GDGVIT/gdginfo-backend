from tornado.web import Application, RequestHandler
from tornado.gen import coroutine, sleep
from tornado.ioloop import IOLoop
from tornado.options import parse_command_line, define, options
from tornado.httpserver import HTTPServer
import requests
from pymongo import MongoClient
import json

conn=MongoClient("localhost",27017)
#db = conn['githubleaderboard']
db= MongoClient("mongodb://apuayush:qwerty1234@ds137110.mlab.com:37110/githubleaderboard")["githubleaderboard"]
coll1=db['score']
coll2=db['top']

define("port", default=9125, help="run on the given port", type=int)
# os.environ.get()

class UpdateWeeklyScore(RequestHandler):
    @coroutine
    def get(self):
        while True:
            d = dict()
            projects_name = []
            #payload = {'client_id': 'e63b429174efcee3f453', 'client_secret': 'baf28b3b72e252c8d54180bfa0b9706e90caa33c','per_page':100}
            for projects in requests.get("https://api.github.com/orgs/GDGVIT/repos?client_id=e63b429174efcee3f453&client_secret=baf28b3b72e252c8d54180bfa0b9706e90caa33c&per_page=62&type=all").json():
                try:
                    projects_name.append(
                        [projects['contributors_url'], projects['stargazers_count'], projects['watchers_count'],
                         projects['forks_count'], projects['open_issues'],projects['name']])
                except:
                    pass

            #payload={'client_id':'e63b429174efcee3f453','client_secret':'baf28b3b72e252c8d54180bfa0b9706e90caa33c'}

            for project in projects_name:
                all_contr=[]
                pat=requests.get(project[0]+"?client_id=e63b429174efcee3f453&client_secret=baf28b3b72e252c8d54180bfa0b9706e90caa33c&per_page=62&type=all")

                if pat.status_code!=204:
                    for contributors in pat.json():
                        all_contr.append(contributors['login'])
                        """initializing a dictionary member with value as zero for a future new member"""
                        if contributors['login'] not in d.keys():
                            d[contributors['login']] = 0

                        d[contributors['login']] += project[1] * 10 + project[2] * 5 + project[3] * 15 + project[4] * 10 + contributors['contributions'] * 40
                try:
                    db.coll2.update({'repo':project[5]},{"$set":{'repo':project[5],'top':all_contr[0]}},upsert=True)
                except:
                    pass
            for members in d.keys():
                if db.coll1.find_one({'username':members}) == None:
                    db.coll1.update({'username': members},
                                                     {"$set": {'score': 0, 'username': members}},
                                                     upsert=True)
                db.coll1.update({'username': members},
                                                 {"$set": {'score': d[members] -
                                                    db.coll1.find_one({'username':members})['score'],'username':members}},
                                                 upsert=True)
                d[members] = 0

            yield sleep(7 * 24 * 60 * 60)


if __name__ == "__main__":
    parse_command_line()
    app = Application(handlers=[(r'/', UpdateWeeklyScore)], db=db,debug=True)
    server = HTTPServer(app)
    server.listen(options.port)
    IOLoop.instance().start()
