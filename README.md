# URLShortner

URLShortner is a service similar to bit.ly. It accepts short and long url pairs which are stored in a Cassandra database. It also stores some pairs in a Redis cluster as a cache. This service uses a writer architecture to reduce response times.

## Installation 
Clone this repository
```bash
git clone https://github.com/ArshD1230/URLShortner.git
```

## Usage
```bash
cd URLShortner
./startService IP1 IP2 IP3 ...
```
where IP1 IP2 IP3 ... are the IP addresses of the nodes you wish to run this service on.

To make a PUT request:
```bash
curl -X PUT IP1:8080/?short=ex\&long=example.org
```
To make a GET request:
```bash
curl IP1:8080/ex
```
