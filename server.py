#!/usr/bin/python3
import threading
import paramiko, base64
import sys
from json import dumps, loads, JSONEncoder, JSONDecoder

from flask import Flask, json, Response
from flask_cors import CORS, cross_origin

import settings as s
import crawler as c
import who

logger = s.logging.getLogger()
s.getargs(logger)

# clears db if needed
# mongologs.drop()

threading.Thread(target=c.spawnThreads, daemon=True).start()

app = Flask(__name__)
CORS(app)

@app.route("/api/master")
@cross_origin()
def api_master():
    js = json.dumps({'response': c.whoCache})
    resp = Response(js, status=200, mimetype='application/json')
    return resp

@app.route("/api/counts")
@cross_origin()
def api_counts():
    js = json.dumps({'response': who.freeLabCount(c.whoCache)})
    resp = Response(js, status=200, mimetype='application/json')
    return resp

@app.route("/api/lastfound/<career_acc>")
@cross_origin()
def api_lastfound(career_acc):
    js = json.dumps({'response': c.lastFound(career_acc)})
    resp = Response(js, status=200, mimetype='application/json')
    return resp

@app.route("/api/cluster/<cluster_name>")
@cross_origin()
def api_cluster(cluster_name):
    js = json.dumps({'response': c.whoCache[cluster_name]})
    resp = Response(js, status=200, mimetype='application/json')
    return resp

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=s.PORT)
