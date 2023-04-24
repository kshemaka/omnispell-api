import flask
from flask_cors import CORS

import main

app = flask.Flask(__name__)
CORS(app, origins="http://localhost:8000")


@app.get("/cards/random-commander")
def index():
    return main.random_commander(flask.request)


if __name__ == '__main__':
    app.run(host="localhost", port=8080, debug=True)
