define({ "api": [
  {
    "type": "get",
    "url": "/repos",
    "title": "data related to repos",
    "name": "data_related_to_repos",
    "group": "all",
    "parameter": {
      "examples": [
        {
          "title": "response-example",
          "content": "{\n    status: 200,\n    message: \"OK\",\n    payload: [\n        {\n            ref: {\n                target: {\n                    history: {\n                        edges: [\n                                    {\n                                        node: {\n                                            deletions: 1,\n                                            additions: 1,\n                                            author: {\n                                                date: \"2019-06-04T20:37:49+05:30\",\n                                                name: \"Angad Sharma\"\n                                                }\n                                        }\n                                    }\n                                ]\n                            }\n                    }\n            },\n            name: \"github-orgs-api\"\n            }]",
          "type": "json"
        }
      ]
    },
    "version": "0.0.0",
    "filename": "./api_server.py",
    "groupTitle": "all"
  },
  {
    "type": "get",
    "url": "/seed",
    "title": "manually seed cache",
    "name": "manually_seed_cache",
    "group": "all",
    "version": "0.0.0",
    "filename": "./api_server.py",
    "groupTitle": "all"
  },
  {
    "type": "get",
    "url": "/leaderboard",
    "title": "org leaderboard",
    "name": "org_leaderboard",
    "group": "all",
    "parameter": {
      "examples": [
        {
          "title": "response-example",
          "content": "{\n    status: 200,\n    message: \"OK\",\n    payload: {\n        L04DB4L4NC3R: 82,\n        Angad Sharma: 16816,\n        bhaveshgoyal27: 19,\n        dependabot-preview[bot]: 3743,\n        shashu421: 2150,\n        HRITISHA: 1105,\n        alan478: 8805,\n        Krishn157: 930\n    }\n}",
          "type": "json"
        }
      ]
    },
    "version": "0.0.0",
    "filename": "./api_server.py",
    "groupTitle": "all"
  },
  {
    "type": "get",
    "url": "/topcontributors",
    "title": "top contributors of the org",
    "name": "top_contributors_of_the_org",
    "group": "all",
    "parameter": {
      "examples": [
        {
          "title": "response-example",
          "content": "{\n    status: 200,\n    message: \"OK\",\n    payload: {\n        CodeCombat: \"Angad Sharma\",\n        skin-cancer-detection: \"shashu421\",\n        cc-website-prototype-19: \"HRITISHA\",\n        github-orgs-api: \"Angad Sharma\",\n        digital-beacon: \"Angad Sharma\",\n        vit-tourist-guide: \"alan478\",\n        DevSoc2K19-Website: \"Angad Sharma\",\n        love-open-source: \"Angad Sharma\",\n        notes-map-analytics: \"Angad Sharma\",\n        smart-park: \"Angad Sharma\",\n        webinars: \"L04DB4L4NC3R\"\n    }\n}",
          "type": "json"
        }
      ]
    },
    "version": "0.0.0",
    "filename": "./api_server.py",
    "groupTitle": "all"
  }
] });
