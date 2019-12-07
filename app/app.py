from flask import Flask, request, jsonify
import os
from redis import Redis
from rq import Queue
import logging

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(name)s - %(message)s', level=logging.DEBUG)
logger = logging.getLogger(__file__)

app = Flask(__name__)

REDIS_URL = os.getenv('REDIS_URL', 'redis://127.0.0.1:6379')
redis_conn = Redis.from_url(REDIS_URL)
q = Queue(connection=redis_conn)


@app.route('/download', methods=['POST'])
def download():
    yt_url = request.json.get('url', '')
    if not yt_url.strip():
        return jsonify({"error": "Url can not be empty."}), 400

    try:
        job = q.enqueue('download', yt_url)
        logger.debug(job)
        return jsonify({"job_id": job.id})
    except Exception as e:
        logger.error("Unexpected error: ", e)
        return jsonify({"error": f"Service unavailable: {e}"}), 500


@app.route('/list_jobs', methods=['GET'])
def list_jobs():
    queued_jobs_ids = q.get_job_ids()
    return jsonify(queued_jobs_ids)


FLASK_HOST = os.getenv('FLASK_HOST', '127.0.0.1')
FLASK_PORT = os.getenv('FLASK_PORT', 5000)
if __name__ == '__main__':
    app.run()
