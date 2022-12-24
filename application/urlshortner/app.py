from flask import Flask, json, request, Response
from datetime import date
from redis import Redis, RedisError
from cassandra.cluster import Cluster
from cassandra.query import tuple_factory
import socket

redis = Redis(host="redis-master", port=6379, db=0)
api = Flask(__name__)
cluster = Cluster(['10.11.1.101'])
session = cluster.connect()
session.execute(
    "CREATE KEYSPACE IF NOT EXISTS urlShortner_keyspace WITH replication = { 'class' : 'SimpleStrategy', 'replication_factor' : 2}")
session.execute("USE urlShortner_keyspace")
session.execute(
    "CREATE TABLE IF NOT EXISTS urls (shortURL text PRIMARY KEY, longURL text )")


@api.route('/<shortURL>', methods=['GET'])
def get_urls(shortURL):
    if shortURL == "":
        return Response(status=400)
    resp = Response(status=307)
    with open('/app/requests.log', 'a') as f:
        f.write("GET {0}\n".format(request.path))
    if (redis.hexists("urls", shortURL)):
        resp.headers['Location'] = redis.hget("urls", shortURL)
    else:
        session.row_factory = tuple_factory
        query = "SELECT * FROM urls WHERE shortURL=?"
        prepared = session.prepare(query)
        row = session.execute(prepared, (str(shortURL)))
        if row:
            resp.headers['Location'] = row[0][1]
        else:
            resp = Response(status=404)
    return resp


@api.route('/', methods=['PUT'])
def put_urls():
    shortURL = request.args.get('short')
    longURL = request.args.get('long')
    if (not shortURL) or (not longURL):
        return Response(status=400)
    with open('/app/requests.log', 'a') as f:
        f.write("PUT {0}\n".format(request.full_path))
    redis.publish('writeRequests', "{0} {1}".format(shortURL, longURL))
    return Response(status=200)


if __name__ == '__main__':
    api.run(host='0.0.0.0', port=80)
