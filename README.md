Build on top of [youtube-dl](https://github.com/ytdl-org/youtube-dl).

Download videos from youtube.com or other video platforms to Dropbox.

### Start services

Update `.env` file:

```
REDIS_URL=redis://redis:6379
```

```
docker-compose -f docker-compose.yml up --build -d
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
