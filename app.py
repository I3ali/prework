"""
    Example app that integrates with Redis, MongoDB,
    and saves/gets Homer Simpson quotes.
"""

from os import environ
from dotenv import load_dotenv
import json
import redis
import requests
from flask import Flask, redirect, jsonify
from pymongo import MongoClient

# Load environment variables from .env file
load_dotenv()

VERSION = "1.1.9-dev"
REDIS_ENDPOINT = environ.get("REDIS_ENDPOINT", "localhost")
REDIS_PORT = int(environ.get("REDIS_PORT", "6379"))
MONGO_URI = environ.get("MONGO_URI")
MONGO_CERT = environ.get("MONGO_CERT", "X509-cert-8417019844152440938.pem")


APP = Flask(__name__)

red = redis.StrictRedis(
    host=REDIS_ENDPOINT, port=REDIS_PORT, db=0, decode_responses=True
)

db = None
test_collection = None


def get_mongo_client():
    global db, test_collection
    if db is None:
        client = MongoClient(
            MONGO_URI,
            uuidRepresentation="standard",
            tlsCertificateKeyFile=MONGO_CERT,
        )
        db = client["Springfield"]
        test_collection = db["Simpson"]
    return test_collection


@APP.route("/")
def redisapp():
    """Main redirect"""
    return redirect("/get", code=302)


@APP.route("/set")
def set_var():
    """Set the quote"""
    request = requests.get(
        "https://thesimpsonsquoteapi.glitch.me/quotes?character=homer simpson",
        timeout=5,
    )
    content = json.loads(request.text)
    quote = content[0]["quote"]
    red.set("quote", quote)
    # MongoDB to store each new quote
    # test_collection.insert_one({"quote": quote})
    return jsonify({"quote": str(red.get("quote"))})


@APP.route("/get")
def get_var():
    """Get the quote"""
    return jsonify({"quote": str(red.get("quote"))})


@APP.route("/reset")
def reset():
    """Reset the quote"""
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
        red.ping()
    except redis.exceptions.ConnectionError:
        return jsonify({"ping": "FAIL"})

    return jsonify({"ping": red.ping()})


@APP.route("/readyz")
def ready():
    """Check the app readiness"""
    return health()


@APP.route("/mongo-test")
def mongo_test() -> dict:
    """Insert a document into MongoDB, retrieve it and clean up"""

    test_collection = get_mongo_client()
    # Insert a test document
    test_doc = {"name": "Homer Simpson", "quote": "D'oh!"}
    result = test_collection.insert_one(test_doc)

    retrieved_doc = test_collection.find_one(
        {"_id": result.inserted_id},
        {"_id": 0}
    )

    # clean up
    test_collection.delete_one({"_id": result.inserted_id})
    return retrieved_doc


if __name__ == "__main__":
    env = environ.get("FLASK_ENV")
    port = environ.get("FLASK_PORT", "8080")
    host = environ.get("FLASK_HOST", "127.0.0.1")
    APP.run(debug=env != "production", host=host, port=int(port))
