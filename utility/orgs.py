import requests


def get_orgs(token):
    print("[RUNNING] get_orgs")
    url = "https://api.github.com/graphql"
    headers = {'Authorization': 'token %s' % token}
    json = {
        "query": """
                    {
                        viewer {
                            organizations(first:100) {
    	                        nodes{
				    name
                                    url
      	                            login
                                    avatarUrl
                                    websiteUrl
                                    description
                                    }
                            }
                        }
                    }
                """
    }
    ret = requests.post(url=url, json=json, headers=headers)
    ret = ret.json()
    return ret

def get_user_data(token):
    url = "https://api.github.com/user"
    headers = {'Authorization': 'token %s' % token}
    ret = requests.get(url=url, headers=headers)
    return ret.json()

