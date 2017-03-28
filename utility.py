# Tornado libraries
from tornado.ioloop import IOLoop
from tornado.web import RequestHandler, Application, asynchronous, removeslash
from tornado.httpserver import HTTPServer
from tornado.httpclient import AsyncHTTPClient
from tornado.gen import engine, Task, coroutine, Return

# Other libraries
import requests
import env

db = env.MOTOR_CLIENT

class UpdateWeeklyScore(RequestHandler):
    """This class calculates the score of each member of the organization in coll1 and top contributors of all the
    repositories in coll2. It calculates the score based on their weekly contribution on the organization."""

    @coroutine
    def get(self):
        while True:
            d = dict()
            projects_name = []

            for projects in requests.get(env.REPO_LINK+env.API_CREDENTIALS).json():

                # scrolling through all the repos of github organization GDGVIT


                try:
                    """ projects_name is a list whose each index contains another list with url of all the contributors
                     of a repo, no. of stars,watchers, forks on the repo in projects variable in index 0,1,2,3,4
                     and the name of the repo in 5 th index."""

                    projects_name.append(
                        [projects['contributors_url'], projects['stargazers_count'], projects['watchers_count'],
                         projects['forks_count'], projects['open_issues'], projects['name']])

                except:  # if the repository is empty thi will skip it

                    pass

            for project in projects_name:
                all_contr = []
                pat = requests.get(project[0] + env.API_CREDENTIALS)

                if pat.status_code != 204:  # if the repository has no contributor this wont allow it
                    for contributors in pat.json():
                        all_contr.append(
                            contributors['login'])  # all_contr will take all the contributors of repository in project
                        if contributors[
                            'login'] not in d.keys():  # if a new member comes this will initiate him with a 0 score.
                            d[contributors['login']] = 0

                        d[contributors['login']] += project[1] * 10 + project[2] * 5 + project[3] * 15 + project[
                                                                                                             4] * 10 + \
                                                    contributors['contributions'] * 40
                        # this calculates score of each member and update the score of a member on dictionary d
                try:
                    db.coll2.update({'repo': project[5]}, {"$set": {'repo': project[5], 'top': all_contr[0]}},
                                    upsert=True)  # this updates top contributor of all repos on coll2 of database
                except:
                    pass
            for members in d.keys():  # member has name of all members as key and their score as value
                if db.coll1.find_one({
                                         'username': members}) is None:  # if a particular member is not on the database this will make his previous week score as zero
                    db.coll1.update({'username': members},
                                    {"$set": {'score': 0, 'username': members}},
                                    upsert=True)

                db.coll1.update({'username': members},
                                {"$set": {'score': d[members] -
                                                   db.coll1.find_one({'username': members})['score'],
                                          'username': members}},
                                upsert=True)  # updateing score of each member on database subtracted by his previous week score
                d[members] = 0

            yield sleep(7 * 24 * 60 * 60)  # this makes the server to sleep for one week


if __name__ == "__main__":
    parse_command_line()
    app = Application(handlers=[(r'/', UpdateWeeklyScore)], db=db, debug=True)
    server = HTTPServer(app)
    server.listen(options.port)
    IOLoop.instance().start()
