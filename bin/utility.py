import requests
import sys
import datetime
import json


def extract_repos(token, org, redis):

    url = 'https://api.github.com/graphql'
    headers = {'Authorization': 'token %s' % token}
    time = datetime.datetime.utcnow() - datetime.timedelta(days=15)
    time = time.isoformat()
    json = {
            "query": """
                    {
                    organization(login: "%s") {
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
                                        deletions
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
                   """ % (
                    org,
                    time)
        }

    # To escape the NoneType object issue when internet is slow
    repos = None
    while repos == None:
        try:
            print('hiding here')
            ret = requests.post(url=url, json=json, headers=headers)
            ret = ret.json()
            repos = ret['data']['organization']['repositories']['nodes']
        except:
            pass
    return repos

def cache_response(token, org, redis):
    data = extract_repos(token, org, redis)
    r = redis.StrictRedis()
    r.execute_command('JSON.SET', 'object', '.', json.dumps(data))

def get_cached_response(org, redis):
    r = redis.StrictRedis()
    reply = json.loads(r.execute_command('JSON.GET', 'object'))
    return reply


def leaderboard(token, org, redis):
    member_list = dict()
    score = dict()
    repos = extract_repos(token, org, redis)
    for i in repos:
        try:
            contributor_edges = i['ref']['target']['history']['edges']
        except:
            continue
        for j in contributor_edges:
            contr = j['node']['author']['name']
            prev_add = 0
            total_commits = 0
            prev_del = 0
            try:
                total_commits = member_list[contr]['commits']
                prev_add = member_list[contr]['additions']
                prev_del = member_list[contr]['deletions']
            except: pass
            total_commits = total_commits + 1
            additions = prev_add + int(j['node']['additions'])
            deletions = prev_del + int(j['node']['deletions'])
            member_list[contr] = {
                'commits': total_commits,
                'additions': additions,
                'deletions': deletions
            }

            score[contr] = total_commits * 10 + additions*5 + deletions * 2

    return score


def topcontributor(token, org, redis):
    member_list = dict()
    top_contributor = dict()
    repos = extract_repos(token, org, redis)
    for i in repos:
    	repo_name = i['name']
    	count = dict()
    	try:
    		repo_contrs = i['ref']['target']['history']['edges']
    	except:
        	continue

    	if len(repo_contrs) == 0:
    		continue

    	for contrs in repo_contrs:
    		try:
    			count[contrs['node']['author']['name']] += 1
    		except:
    			count[contrs['node']['author']['name']] = 1
    	top_contributor[repo_name] = max(count, key=count.get)

    return top_contributor

# TODO - top_contributors we will see later right now api limit exceeded
