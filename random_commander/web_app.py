import flask

import main

app = flask.Flask(__name__)


@app.get("/cards/random-commander")
def index():
    return main.random_commander(flask.request)


if __name__ == '__main__':
    app.run(host="localhost", port=8080, debug=True)
