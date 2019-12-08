Self-hosted service to download videos from youtube.com or other video platforms to Dropbox.

Build on top of [youtube-dl](https://github.com/ytdl-org/youtube-dl) and [RQ](https://python-rq.org/docs/results/).

### Start services

Copy `.env.sample` to `.env`, and provide necessary environment variables, like `DROPBOX_ACCESS_TOKEN`.

```
docker-compose -f docker-compose.yml up --build -d
```

### Usage example

Service provides endpoint where you could send video url that will be downloaded and uploaded to specific Dropbox folder.

```
curl -X POST \
  http://127.0.0.1:5000/download \
  -H 'Accept: */*' \
  -H 'Accept-Encoding: gzip, deflate' \
  -H 'Cache-Control: no-cache' \
  -H 'Connection: keep-alive' \
  -H 'Content-Length: 57' \
  -H 'Content-Type: application/json' \
  -H 'Host: 127.0.0.1:5000' \
  -H 'Postman-Token: 740c2fb6-abc0-44e7-9f36-19e84bd79f13,292952af-9fad-494b-a259-40ef34f3b5ce' \
  -H 'User-Agent: PostmanRuntime/7.20.1' \
  -H 'cache-control: no-cache' \
  -d '{
	"url": "https://www.youtube.com/watch?v=SsFI40bXROs"
}'
```

### Start Redis locally

```
docker-compose -f docker-compose.redis.yml up --build --remove-orphans
```

Update `.env` file to run application separately:

```
REDIS_URL=redis://127.0.0.1:6379
```

Connect to Redis:

```
redis-cli -h 127.0.0.1 -p 6379
```

Show all keys:

```
127.0.0.1:6379> keys *
```
