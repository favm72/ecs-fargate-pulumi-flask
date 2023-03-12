import json
from flask import Flask, make_response
app = Flask(__name__)


@app.get('/')
def hello():
    return make_response(json.dumps({
        "message": "Hello from Pulumi!"
    }), 200)


@app.get('/data')
def data():
    return make_response(json.dumps([
        {"id": 1, "name": "John"},
        {"id": 2, "name": "Jane"},
        {"id": 3, "name": "Jack"}
    ]), 200)


if __name__ == "__main__":
    app.run(debug=True, port=5000)
