import random
import time
import urllib.parse

import flask
import requests


def retrieve_data():
    d = list()
    query = '(game:paper) not:ub is:commander -o:partner -o:background'
    url = 'https://api.scryfall.com/cards/search?q=' + urllib.parse.quote_plus(query)
    r = requests.get(url)
    while r.status_code == 200:
        json = r.json()
        d.extend(json['data'])
        if json['has_more']:
            time.sleep(0.1)
            r = requests.get(json['next_page'])
        else:
            break
    return d


data = retrieve_data()


def random_commander(request: flask.Request) -> flask.Response:
    if len(data) > 0:
        card = data[random.randrange(0, len(data))]
        return flask.jsonify(card)
    else:
        return flask.Response(status=500)
