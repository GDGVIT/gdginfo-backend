## github-orgs-api
---

For calculating score of all members of any github organisation and top contributors of all repositories.

[![view original](https://img.shields.io/badge/upstream-view%20source%20repo-orange.svg)](https://github.com/GDGVIT/gdginfo-backend.git) [![docs](https://img.shields.io/badge/docs-view%20API%20documentation-brightgreen.svg)](https://l04db4l4nc3r.github.io/github-orgs-api/)

<br/>

### Some features

- [X] GitHub Graph API
- [X] Interchangable organization leaderboard
- [X] Top contributors for organizations
- [X] Repository specific metadata for organizations
- [X] Pluggable caching layer 
- [X] Automatic Scheduled cache update
- [X] Manual cache update
- [X] GitHub Oauth

<br/>

### Getting Started

You can use this application easily just by changing the following credentials..

* Redis server url (optional)
* Name of the organization
* Github api key

This project uses `.env`. To configure, simply make a file named *.env* in the root of your project and add the following lines to it.

```
# organization handle on GitHub 
ORGANIZATION=<Name of the organization as specified in GitHub>

# redis URI
REDIS_URL=<your redis url>

# GitHub client ID
GITHUB_CLIENT_ID=<your-id>

# GitHub client secret
GITHUB_CLIENT_SECRET=<your-secret>
```

<br/>

### How to use

Clone the repository and add the above credentials.

```bash
# Clone the repo
$ git clone https://github.com/GDGVIT/gdginfo-backend.git

# Navigate into it
$ cd gdginfo-backend

# Bootstrap
$ make
```

<br/>

### Ways to run

*	**Regular mode**: run this if you do not want a caching layer in your application. Will drastically increase response time but save the cost of having a caching service

```
$ ./app
```

<br/>

* **Caching mode**: run this if you want a caching layer in your application. Will drastically decrease response latency.

```
$ ./app --with-cache
```
<br/>

### Clean
Uninstall all requirements that were installed while making this project. 
```
$ make clean
```

<br/>

### Generate docs
Generate documentation based on comment descriptions on the APIs. This uses `apidoc` and requires `npm`.
```
$ make docs
```
<br/>

### How it works

**Algorithm**: It uses github api and fetches the information about members, all the repositories in that organization, 
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

```python
d[contributors['login']] += project[1] * 10 + project[2] * 5 +project[3] * 15 + contributors['contributions'] * 40
```
<br/>

**Caching**: When the `--with-cache` flag is provided, all responses are served from a cache. This cache is updated daily. This significantly decreases response latency since github api provides only 10 requests per minute. 


<br/>

### Limitations

* Only 30 repositories can be fetched from the API at one time.
* Only 10 requests can be made to the API per minute.

<br/>

### Mitigation

* Pluggable caching layer
* Manual cache seed
* CRON-ed cache seed

<br/>

### Built With

* [GithubApi](https://developer.github.com/v3/) 

### Built by
* [GDGVIT](https://www.gdgvitvellore.com)

### Contributors

* Shubham Bhardwaj
* Apurva Nitanjay
* Angad Sharma

