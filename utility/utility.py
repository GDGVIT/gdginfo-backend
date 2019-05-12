import requests
import sys
import datetime
import pickle

def extract_repos(token, org, redis):
    print("[RUNNING] extract_repos")
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

def cache_response(token, org, rd):
    print("[RUNNING] cache_response")
    data = extract_repos(token, org, rd)
    pickled_object = pickle.dumps(data)
    print(rd)
    if not rd.set(org, pickled_object):
        print("[ERROR] setting in redis: cache_response")
    else:
       print("[COMPLETED] cache_response")
    

def get_cached_response(org, redis):
    print("[RUNNING] get_cached_response")
    unpacked_pickled_object = pickle.loads(redis.get(org))
    return unpacked_pickled_object

def repos(token, org, redis):
    if redis is None:
        repos = extract_repos(token, org, redis)
    else:
        repos = get_cached_response(org, redis)
    return repos

def leaderboard(token, org, redis):
    member_list = dict()
    score = dict()
    if redis is None:
        repos = extract_repos(token, org, redis)
    else:
        repos = get_cached_response(org, redis)
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
    if redis is None:
        repos = extract_repos(token, org, redis)
    else:
        repos = get_cached_response(org, redis)
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
