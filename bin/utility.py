# Other libraries
import time
import requests
import env

db = env.MONGO_CLIENT
coll1 = db['score']
coll2 = db['top']

while True:
    d = {}
    projects_name = []
    members_name = []
    for members in requests.get(env.MEMBERS_LINK).json():
        members_name.append(members['login'])

    for projects in requests.get(env.REPO_LINK).json():

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
        pat = requests.get(project[0] + env.API_CREDENTIALS)

        if pat.status_code != 204:
            for contributors in pat.json():

                if(contributors['login'] in members_name):
                    all_contr.append(contributors['login'])

                    if contributors['login'] not in d.keys():
                        d[contributors['login']] = 0

                    d[contributors['login']] += project[1] * 10 + project[2] * 5
                    + project[3] * 15 + project[4] * 10
                    + contributors['contributions'] * 40

        try:
            db.coll2.update({'repo': project[5]},
                            {"$set": {'repo': project[5], 'top': all_contr[0]}},
                            upsert=True)
        except:
            pass

    for members in d.keys():
        if db.coll1.find_one({'username': members}) is None:
            db.coll1.update({'username': members},
                            {"$set": {'score': 0, 'username': members}},
                            upsert=True)
        member_score = db.coll1.find_one({'username': members})['score']
        db.coll1.update({'username': members},
                        {"$set": {'score': d[members] - member_score,
                                  'username': members}}, upsert=True)
        d[members] = 0

    time.sleep(7 * 24 * 60 * 60)
