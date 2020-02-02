define({ "api": [
  {
    "type": "get",
    "url": "/analyze",
    "title": "analyze a repository",
    "name": "analyze_a_repository",
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "optional": false,
            "field": "org",
            "description": "<p>organization name</p>"
          },
          {
            "group": "Parameter",
            "optional": false,
            "field": "repo",
            "description": "<p>repository name for the organization</p>"
          }
        ]
      }
    },
    "group": "all",
    "permission": [
      {
        "name": "logged-in"
      }
    ],
    "version": "0.0.0",
    "filename": "routes/analyze.py",
    "groupTitle": "all"
  },
  {
    "type": "get",
    "url": "/json/analyze",
    "title": "analyze a repository and spit out JSON",
    "name": "analyze_a_repository_and_spit_out_JSON",
    "group": "all",
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "optional": false,
            "field": "org",
            "description": "<p>organization name</p>"
          },
          {
            "group": "Parameter",
            "optional": false,
            "field": "repo",
            "description": "<p>repository name for the organization</p>"
          }
        ]
      },
      "examples": [
        {
          "title": "response-example",
          "content": "{\n\"gitinspector\": {\n\"version\": {\n\"$\": \"0.4.4\"\n},\n\"repository\": {\n\"$\": \"GDGVIT_template\"\n},\n\"report-date\": {\n\"$\": \"2020/01/27\"\n},\n\"changes\": {\n\"message\": {\n\"$\": \"The following historical commit information, by author, was found in the repository\"\n},\n\"authors\": {\n\"author\": [{\n\"name\": {\n\"$\": \"Angad Sharma\"\n},\n\"gravatar\": {\n\"$\": \"https://www.gravatar.com/avatar/5e8def242c2dd4eede4822fe2f8944b4?default=identicon\"\n},\n\"commits\": {\n\"$\": 1\n},\n\"insertions\": {\n\"$\": 1\n},\n\"deletions\": {\n\"$\": 0\n},\n\"percentage-of-changes\": {\n\"$\": 1.82\n}\n},\n{\n\"name\": {\n\"$\": \"L04DB4L4NC3R\"\n},\n\"gravatar\": {\n\"$\": \"https://www.gravatar.com/avatar/5053cc8b4421a2e1f55a238b00430ace?default=identicon\"\n},\n\"commits\": {\n\"$\": 1\n},\n\"insertions\": {\n\"$\": 53\n},\n\"deletions\": {\n\"$\": 1\n},\n\"percentage-of-changes\": {\n\"$\": 98.18\n}\n}\n]\n}\n},\n\"blame\": {\n\"message\": {\n\"$\": \"Below are the number of rows from each author that have survived and are still intact in the current revision\"\n},\n\"authors\": {\n\"author\": {\n\"name\": {\n\"$\": \"L04DB4L4NC3R\"\n},\n\"gravatar\": {\n\"$\": \"https://www.gravatar.com/avatar/5053cc8b4421a2e1f55a238b00430ace?default=identicon\"\n},\n\"rows\": {\n\"$\": 53\n},\n\"stability\": {\n\"$\": 100.0\n},\n\"age\": {\n\"$\": 0.0\n},\n\"percentage-in-comments\": {\n\"$\": 0.0\n}\n}\n}\n},\n\"timeline\": {\n\"message\": {\n\"$\": \"The following history timeline has been gathered from the repository\"\n},\n\"periods\": {\n\"@length\": \"week\",\n\"period\": {\n\"name\": {\n\"$\": \"2020W03\"\n},\n\"authors\": {\n\"author\": [{\n\"name\": {\n\"$\": \"Angad Sharma\"\n},\n\"gravatar\": {\n\"$\": \"https://www.gravatar.com/avatar/5e8def242c2dd4eede4822fe2f8944b4?default=identicon\"\n},\n\"work\": {\n\"$\": \".\"\n}\n},\n{\n\"name\": {\n\"$\": \"L04DB4L4NC3R\"\n},\n\"gravatar\": {\n\"$\": \"https://www.gravatar.com/avatar/5053cc8b4421a2e1f55a238b00430ace?default=identicon\"\n},\n\"work\": {\n\"$\": \"+++++++++++++++++++++++\"\n}\n}\n]\n},\n\"modified_rows\": {\n\"$\": 55\n}\n}\n}\n},\n\"metrics\": {\n\"message\": {\n\"$\": \"No metrics violations were found in the repository\"\n}\n},\n\"responsibilities\": {\n\"message\": {\n\"$\": \"The following responsibilities, by author, were found in the current revision of the repository (comments are excluded from the line count, if possible)\"\n},\n\"authors\": {\n\"author\": {\n\"name\": {\n\"$\": \"L04DB4L4NC3R\"\n},\n\"gravatar\": {\n\"$\": \"https://www.gravatar.com/avatar/5053cc8b4421a2e1f55a238b00430ace?default=identicon\"\n},\n\"files\": {\n\"file\": {\n\"name\": {\n\"$\": \"README.md\"\n},\n\"rows\": {\n\"$\": 53\n}\n}\n}\n}\n}\n},\n\"extensions\": {\n\"message\": {\n\"$\": \"The extensions below were found in the repository history\"\n},\n\"used\": {\n\"extension\": {\n\"$\": \"md\"\n}\n},\n\"unused\": {}\n}\n}\n}",
          "type": "json"
        }
      ]
    },
    "permission": [
      {
        "name": "logged-in"
      }
    ],
    "version": "0.0.0",
    "filename": "routes/analyze.py",
    "groupTitle": "all"
  },
  {
    "type": "get",
    "url": "/repos",
    "title": "data related to repos",
    "name": "data_related_to_repos",
    "group": "all",
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "optional": false,
            "field": "org",
            "description": "<p>organization name</p>"
          }
        ]
      },
      "examples": [
        {
          "title": "response-example",
          "content": "{\n    status: 200,\n    message: \"OK\",\n    payload:\n        {\n\"name\": \"CodeCombat\",\n\"ref\": {\n\"target\": {\n\"history\": {\n\"edges\": [{\n\"node\": {\n\"author\": {\n\"name\": \"Angad Sharma\",\n\"date\": \"2019-06-06T08:38:08+05:30\"\n},\n\"additions\": 3,\n\"deletions\": 27,\n\"pushedDate\": \"2019-06-06T03:08:09Z\",\n\"message\": \"Merge pull request #8 from CodeChefVIT/dependabot/npm_and_yarn/mongoose-5.5.13\\n\\nBump mongoose from 5.5.12 to 5.5.13\",\n\"messageBody\": \"\\u2026se-5.5.13\\n\\nBump mongoose from 5.5.12 to 5.5.13\",\n\"url\": \"https://github.com/CodeChefVIT/CodeCombat/commit/60e45681c9baf8b02c2996ffc14442741f0c6fea\"\n}\n}]\n\n                        }\n                }\n            }\n        }",
          "type": "json"
        }
      ]
    },
    "permission": [
      {
        "name": "logged-in"
      }
    ],
    "version": "0.0.0",
    "filename": "routes/repos.py",
    "groupTitle": "all"
  },
  {
    "type": "get",
    "url": "/orgs",
    "title": "get a list of organizations",
    "name": "get_a_list_of_organizations",
    "group": "all",
    "permission": [
      {
        "name": "logged-in"
      }
    ],
    "parameter": {
      "examples": [
        {
          "title": "response-example",
          "content": "{\n  \"data\": {\n    \"viewer\": {\n      \"organizations\": {\n        \"nodes\": [\n          {\n            \"name\": \"DSC VIT Vellore\",\n            \"url\": \"https://github.com/GDGVIT\",\n            \"login\": \"GDGVIT\",\n            \"avatarUrl\": \"https://avatars0.githubusercontent.com/u/11557748?v=4\",\n            \"websiteUrl\": \"https://dscvit.com/\",\n            \"description\": \"Google Developers Group VIT\"\n          },\n          {\n            \"name\": \"CodeChef - VIT Vellore\",\n            \"url\": \"https://github.com/CodeChefVIT\",\n            \"login\": \"CodeChefVIT\",\n            \"avatarUrl\": \"https://avatars2.githubusercontent.com/u/31820857?v=4\",\n            \"websiteUrl\": \"www.codechefvit.com\",\n            \"description\": \"CodeChef is a technical chapter in VIT University Vellore that helps students all over the campus to improve their coding skills.\"\n          }\n        ]\n      }\n    }\n  }\n}",
          "type": "json"
        }
      ]
    },
    "version": "0.0.0",
    "filename": "routes/orgs.py",
    "groupTitle": "all"
  },
  {
    "type": "get",
    "url": "/seed",
    "title": "manually seed cache [Hit only once]",
    "name": "manually_seed_cache",
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "optional": false,
            "field": "org",
            "description": "<p>organization name</p>"
          }
        ]
      }
    },
    "permission": [
      {
        "name": "logged-in"
      }
    ],
    "group": "all",
    "version": "0.0.0",
    "filename": "routes/seed.py",
    "groupTitle": "all"
  },
  {
    "type": "get",
    "url": "/leaderboard",
    "title": "org leaderboard",
    "name": "org_leaderboard",
    "group": "all",
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "optional": false,
            "field": "org",
            "description": "<p>organization name</p>"
          }
        ]
      },
      "examples": [
        {
          "title": "response-example",
          "content": "{\n    status: 200,\n    message: \"OK\",\n    payload: {\n        L04DB4L4NC3R: 82,\n        Angad Sharma: 16816,\n        bhaveshgoyal27: 19,\n        dependabot-preview[bot]: 3743,\n        shashu421: 2150,\n        HRITISHA: 1105,\n        alan478: 8805,\n        Krishn157: 930\n    }\n}",
          "type": "json"
        }
      ]
    },
    "permission": [
      {
        "name": "logged-in"
      }
    ],
    "version": "0.0.0",
    "filename": "routes/leaderboard.py",
    "groupTitle": "all"
  },
  {
    "type": "get",
    "url": "/topcontributors",
    "title": "top contributors of the org",
    "name": "top_contributors_of_the_org",
    "group": "all",
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "optional": false,
            "field": "org",
            "description": "<p>organization name</p>"
          }
        ]
      },
      "examples": [
        {
          "title": "response-example",
          "content": "{\n    status: 200,\n    message: \"OK\",\n    payload: {\n        CodeCombat: \"Angad Sharma\",\n        skin-cancer-detection: \"shashu421\",\n        cc-website-prototype-19: \"HRITISHA\",\n        github-orgs-api: \"Angad Sharma\",\n        digital-beacon: \"Angad Sharma\",\n        vit-tourist-guide: \"alan478\",\n        DevSoc2K19-Website: \"Angad Sharma\",\n        love-open-source: \"Angad Sharma\",\n        notes-map-analytics: \"Angad Sharma\",\n        smart-park: \"Angad Sharma\",\n        webinars: \"L04DB4L4NC3R\"\n    }\n}",
          "type": "json"
        }
      ]
    },
    "permission": [
      {
        "name": "logged-in"
      }
    ],
    "version": "0.0.0",
    "filename": "routes/leaderboard.py",
    "groupTitle": "all"
  }
] });
