
data_dir = './data'
discord_secret_token = "TODO: SECRET TOKEN"

# just some helper constants
seconds = 1
minutes = 60 * seconds
hours = 60 * minutes
days = 24 * hours

modules = {
    "basics": {
        "enabled": True,
    },
    "latex": {
        "enabled": True,
    },
    "kattis": {
        "enabled": True,

        "interval": 3*minutes,

        "lists": [
            {
                "channels": ["kattis"],
                "url": "https://open.kattis.com/countries/ISL",
            },
            {
                "channels": ["kattis"],
                "url": "https://iceland.kattis.com/ranklist",
            },
            {
                "channels": ["ioi-thjalfun"],
                "url": "https://ioi.kattis.algo.is/ranklist",
            },
            {
                "channels": ["icpc"],
                "url": "https://icpc.kattis.com/countries/ISL",
            },
        ],
    },
    "events": {
        "enabled": True,

        # clist.by login
        "username": "TODO: USERNAME",
        "api_key": "TODO: API KEY",

        "interval": 5*minutes, # how frequently to fetch new data

        "default_channels": ['keppnir'],
        "default_reminders": [6*days, 3*hours, 30*minutes],

        "calendars": [
            {
                "id": 1,
                "name": "codeforces.com",
                "channels": ['codeforces'],
            },
            {
                "id": 3,
                "name": "uva.onlinejudge.org",
                "channels": ['icpc'],
            },
            {
                "id": 12,
                "name": "topcoder.com",
            },
            {
                "id": 23,
                "name": "hsin.hr/coci",
                "channels": ['ioi-thjalfun', 'keppnir'],
            },
            {
                "id": 35,
                "name": "google.com/codejam",
                "channels": ['codejam'],
            },
            {
                "id": 38,
                "name": "ipsc.ksp.sk",
            },
            {
                "id": 29,
                "name": "facebook.com/hackercup",
            },
            {
                "id": 25,
                "name": "usaco.org",
                "channels": ['ioi-thjalfun', 'keppnir'],
            },
            {
                "id": 63,
                "name": "hackerrank.com",
            },
            {
                "id": 64,
                "name": "codeforces.com/gyms",
                "channels": ['codeforces'],
            },
            {
                "id": 73,
                "name": "hackerearth.com",
            },
            {
                "id": 82,
                "name": "stats.ioinformatics.org",
                "channels": ['ioi-thjalfun', 'keppnir'],
            },
            {
                "id": 2,
                "name": "codechef.com",
            },
            {
                "id": 65,
                "name": "projecteuler.net",
                "channels": ['projecteuler'],
            },
            {
                "id": 91,
                "name": "open.kattis.com",
                "channels": ['kattis'],
            },
            {
                "id": 90,
                "name": "csacademy.com",
            },
            {
                "id": 86,
                "name": "icpc.baylor.edu",
                "channels": ['icpc'],
            },
            {
                "id": 93,
                "name": "atcoder.jp",
            },

        ]
    }
}

