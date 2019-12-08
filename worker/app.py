import os
from redis import Redis
from rq import Worker, Connection
import logging

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(name)s - %(message)s', level=logging.DEBUG)
logger = logging.getLogger(__file__)


def process_queue():
    REDIS_URL = os.getenv('REDIS_URL', 'redis://127.0.0.1:6379')
    redis_conn = Redis.from_url(REDIS_URL)
    with Connection(connection=redis_conn):
        worker = Worker(['default'])
        worker.work()


process_queue()
