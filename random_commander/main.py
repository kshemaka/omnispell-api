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
    if request.method == 'OPTIONS':
        headers = {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'GET',
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Max-Age': '3600'
        }
        return flask.Response(status=204, headers=headers)

    if len(data) > 0:
        card = data[random.randrange(0, len(data))]
        response = flask.jsonify(card)
        response.headers['Access-Control-Allow-Origin'] = '*'
        return response
    else:
        return flask.Response(status=500)
