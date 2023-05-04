import random
import time
import urllib.parse

import flask
import requests


def retrieve_data():
    d = list()
    query = '(game:paper) -st:funny not:ub is:brawlcommander -o:partner -o:background -t:background'
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


def check_legality(card):
    if card['legalities']['commander'] == 'banned':
        return False
    return True


def check_type(card):
    face = card
    if 'card_faces' in card:
        face = card['card_faces'][0]

    if 'Planeswalker' in face['type_line'] and 'commander' not in face['oracle_text']:
        return False
    return True


def check_rarity(card):
    if 'uncommon' in card['rarity']:
        return True
    return False


def filter_data(f):
    d = data.copy()
    if 'brawl' not in f:
        d = [c for c in d if check_legality(c) and check_type(c)]
    if 'pauper' in f:
        d = [c for c in d if check_rarity(c)]
    return d


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
        filtered_data = filter_data(request.args.get('format', 'commander'))
        card = filtered_data[random.randrange(0, len(filtered_data))]
        response = flask.jsonify(card)
        response.headers['Access-Control-Allow-Origin'] = '*'
        return response
    else:
        return flask.Response(status=500)
