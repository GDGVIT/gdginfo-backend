# GDGINFO-Backend

This is the backend for *[GDGVITinfo](https://info.gdgvitvellore.com) used for calculating score of all members of GDGVIT github organisation and top contributors of all repository.


## Getting Started

You can use this application easily just by changing the following credentials..

* Redis server url (optional)
* Name of the organization
* Github api key

This project uses `.env`. To configure, simply make a file named *.env* in the root of your project and add the following lines to it.

```
TOKEN=<Your github token, under developer settings on GitHub>
ORGANIZATION=<Name of the organization as specified in GitHub>
REDIS_URL=<your redis url>
```

<br/>

### How to use

just clone the repository and add the above credentials.

```bash
git clone https://github.com/GDGVIT/gdginfo-backend.git
cd gdginfo-backend
echo "TOKEN=<your-github-access-token>" > .env
echo "ORGANIZATION=<your-github-ORG>" >> .env
echo "REDIS_URL=<your redis URL>" >> .env # optional
```

<br/>
### Ways to run

*	Regular mode: run this if you do not want a caching layer in your application. Will drastically increase response time but save the cost of having a caching service

```
python3 api_server.py
```

* Caching mode: run this if you want a caching layer in your application. Will drastically decrease response latency.

```
python3 api_server.py --with-cache
```
<br/>

## How it works

`Algorithm`: It uses github api and fetches the information about members, all the repositories in that organization, 
members contribution in those repository.
The application scrolls through all the repositories that belong to this organization.
and using that it calculates contribution a particular individual based on his contribution to that repository.


| Action | Weightage |
|:------:|:---------:|
| stargazers count | 10 |
| watchers count | 10 |
| forks count | 15 |
| contributions | 40 |

<br/>

```
d[contributors['login']] += project[1] * 10 + project[2] * 5 +project[3] * 15 + contributors['contributions'] * 40
```
<br/>

`Caching`: When the *--with-cache* flag is provided, all responses are served from a cache. This cache is updated daily. This significantly decreases response latency since github api provides only 10 requests per minute. 


<br/>

## Built With

* [GithubApi](https://developer.github.com/v3/) 

## Built by
* [GDGVIT](https://www.gdgvitvellore.com)

## Contributors

Shubham Bhardwaj
Apurva Nitanjay
Angad Sharma

