# GDGINFO-Backend

This is the backend for *[GDGVITinfo](https://info.gdgvitvellore.com) used for calculating score of all members of GDGVIT github organisation and top contributors of all repository.


## Getting Started

You can use this application easily just by changing the following credentials..
	i-database credentials
	ii-name of the organization
	iii- github api key


### How to use

just clone the repository and add the above credentials.

```
git clone https://github.com/GDGVIT/gdginfo-backend.git
cd gdginfo-backend
echo "TOKEN=<your-github-access-token>" > .env
echo "ORGANIZATION=<your-github-ORG>" >> .env
```

### Ways to run

*	Regular mode

```
python3 api_server.py
```

* Caching mode

```
python3 api_server.py --with-cache
```

## How it works

It uses github api and fetches the information about members, all the repositories in that organization, 
members contribution in those repository.

### Algorithm

The application scrolls through all the repositories that belong to this organization.
and using that it calculates contribution a particular individual based on his contribution to that repository.


| Action | Weightage |
|:------:|:---------:|
| stargazers count | 10 |
| watchers count | 10 |
| forks count | 15 |
| contributions | 40 |


```
d[contributors['login']] += project[1] * 10 + project[2] * 5 +project[3] * 15 + contributors['contributions'] * 40
```

### And coding style tests

This updates the data on the database and if data is not present it will automatically create memory for that.

```
db.coll1.update({'username': members},
                        {"$set": {'score': d[members] - member_score,
                                  'username': members}}, upsert=True)
```

## Note

github api provides only 10 requests per minute. So you need to do the authentication. 


<br/>

## Things that need to be implemented 

- [X] Caching layer
- [ ] CRON job to update cache
- [X] Organization specific cache maintenance
- [ ] Handler for organization login

<br/>

Why this needs to be implemented

* Response latency
* Only 10 requests allowed per minute
* The logic for handling multiple organizations does not exist

<br/>

## Built With

* [GithubApi](https://developer.github.com/v3/) - The api used to get data.

## Built by
* [GDGVIT](https://www.gdgvitvellore.com)

## Contributors

Shubham Bhardwaj
Apurva Nitanjay
Angad Sharma

