import redis
import time
from cassandra.cluster import Cluster
from cassandra.query import tuple_factory

cluster = Cluster(['10.11.1.101'])
session = cluster.connect()
session.execute(
    "CREATE KEYSPACE IF NOT EXISTS urlShortner_keyspace WITH replication = { 'class' : 'SimpleStrategy', 'replication_factor' : 2}")
session.execute("USE urlShortner_keyspace")
session.execute(
    "CREATE TABLE IF NOT EXISTS urls (shortURL text PRIMARY KEY, longURL text )")

r = redis.Redis(host='redis-master', port=6379, db=0)
p = r.pubsub()
p.subscribe('writeRequests')
p.get_message()
while True:
    message = p.get_message()
    if message:
        data = str(message["data"]).split(" ")
        shortURL = data[0][2:]
        if len(data) > 1:
            longURL = data[1][:-1]
            r.hset("urls", shortURL, longURL)
            query = "INSERT INTO urls (shortURL,longURL) VALUES (?, ?)"
            prepared = session.prepare(query)
            session.execute(prepared, (shortURL, longURL))
