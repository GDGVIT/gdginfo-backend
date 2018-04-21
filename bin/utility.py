import requests
import os
import datetime
import env

try:
    token = os.environ['token']
except:
    token = env.token
    pass

print(token)

url = 'https://api.github.com/graphql'
headers = {'Authorization': 'token %s' % token}
def leaderboard():
    member_list = dict()
    time = datetime.datetime.utcnow()-datetime.timedelta(days=7)
    time = time.isoformat()
    json = {
        "query": """
            {
              organization(login: "GDGVIT") {
                repositories(first: 100, affiliations: COLLABORATOR, orderBy: {field: PUSHED_AT, direction: DESC}) {
                  nodes {
                    name
                    ref(qualifiedName: "master") {
                      target {
                        ... on Commit {
                          history(first: 50, since: "%s") {
                            edges {
                              node {
                                author {
                                  name
                                  date
                                }
                                additions
                              }
                            }
                          }
                        }
                      }
                    }
                  }
                }
              }
    }
            """ % time
    }

    # To escape the NoneType object issue when internet is slow
    repos = None
    while repos == None:
        try:
            print('hiding here')
            ret = requests.post(url=url, json=json, headers=headers)
            ret = ret.json()
            repos = ret['data']['organization']['repositories']['nodes']
        except: pass

    for i in repos:
        print(i)
        try:
            contributor_edges = i['ref']['target']['history']['edges']
        except:
            continue
        for j in contributor_edges:
            contr = j['node']['author']['name']
            prev_add = 0
            total_commits = 0
            try:
                total_commits = member_list[contr]['commits']
                prev_add = member_list[contr]['additions']
            except: pass
            total_commits = total_commits + 1
            additions = prev_add + int(j['node']['additions'])
            member_list[contr] = {
                'commits': total_commits,
                'additions': additions,
                'score': total_commits*additions
            }

    return member_list


def top_contributor():

    json = {}
    # print(json)
    ret = requests.post(url=url, json=json, headers=headers)
    return ret.json()

# top_contributor()
leaderboard()