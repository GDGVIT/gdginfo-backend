# Other libraries
import time
import requests
import os
from pymongo import MongoClient
import datetime

db = MongoClient(os.environ['DB_LINK'])['githubleaderboard']
coll1 = db['score']
coll2 = db['top']
d=dict()
rel=dict()

flag = 1
time1 = time.mktime(datetime.datetime.now().timetuple())

while True:
    projects_name = []
    members_name = []
    for members in requests.get(os.environ['MEMBERS_LINK']).json():
        members_name.append(members['login'])

    for projects in requests.get(os.environ['REPO_LINK']).json():

        try:
            projects_name.append([projects['contributors_url'],
                                  projects['stargazers_count'],
                                  projects['watchers_count'],
                                  projects['forks_count'],
                                  projects['open_issues'], projects['name']])

        except:
            pass

    for project in projects_name:
        all_contr = []
        pat = requests.get(project[0] + os.environ['API_CREDENTIALS'])

        if pat.status_code != 204:
            for contributors in pat.json():

                if(contributors['login'] in members_name):
                    all_contr.append(contributors['login'])

                    if contributors['login'] not in d.keys():
                        d[contributors['login']] = 0
                        rel[contributors['login']]=0

                    d[contributors['login']] += project[1] * 10 + project[2] * 5
                    + project[3] * 15 + project[4] * 10
                    + contributors['contributions'] * 40

        try:
            db.coll2.update({'repo': project[5]},
                            {"$set": {'repo': project[5], 'top': all_contr[0]}},
                            upsert=True)
        except:
            pass

    time2 = time.mktime(datetime.datetime.now().timetuple())
    if flag == 1 or time2 - time1 > 7 * 24 * 60 * 60:
        rel = d
        time1 = time2
        flag = 999

    for members in d.keys():
        if db.coll1.find_one({'username': members}) is None:
            db.coll1.update({'username': members},
                            {"$set": {'score': 0, 'username': members}},
                            upsert=True)
        member_score =rel[members]
        db.coll1.update({'username': members},
                        {"$set": {'score': d[members] - member_score,
                                  'username': members}}, upsert=True)
        d[members] = 0
