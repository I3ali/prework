
"""
    Example app that integrates with redis and save/get homer simpson quotes
"""
from os import environ
import json
import redis
import requests
import json
from flask import Flask, redirect, jsonify

VERSION = "1.1.1"
REDIS_ENDPOINT = environ.get("REDIS_ENDPOINT", "localhost")
REDIS_PORT = int(environ.get("REDIS_PORT", "6379"))

APP = Flask(__name__)

@APP.route("/")
def redisapp():
    """Main redirect"""
    return redirect("/get", code=302)

@APP.route("/set")
def set_var():
    """Set the quote"""
    red = redis.StrictRedis(host=REDIS_ENDPOINT, port=REDIS_PORT, db=0, decode_responses=True)

    request = requests.get('https://thesimpsonsquoteapi.glitch.me/quotes?character=homer simpson')
    content = json.loads(request.text)
    quote = content[0]['quote']
    red.set("quote", quote)
    return jsonify({"quote": str(red.get("quote"))})

@APP.route("/get")
def get_var():
    """Get the quote"""
    red = redis.StrictRedis(host=REDIS_ENDPOINT, port=REDIS_PORT, db=0, decode_responses=True)
    return jsonify({"quote": str(red.get("quote"))})

@APP.route("/reset")
def reset():
    """Reset the quote"""
    red = redis.StrictRedis(host=REDIS_ENDPOINT, port=REDIS_PORT, db=0, decode_responses=True)
    red.delete("quote")
    return jsonify({"quote": str(red.get("quote"))})

@APP.route("/version")
def version():
    """Get the app version"""
    return jsonify({"version": VERSION})

@APP.route("/healthz")
def health():
    """Check the app health"""
    try:
        red = redis.StrictRedis(host=REDIS_ENDPOINT, port=REDIS_PORT, db=0, decode_responses=True)
        red.ping()
    except redis.exceptions.ConnectionError:
        return jsonify({"ping": "FAIL"})

    return jsonify({"ping": red.ping()})

@APP.route("/readyz")
def ready():
    """Check the app readiness"""
    return health()

if __name__ == "__main__":
   APP.run(debug=True, host="0.0.0.0")
