FROM python:3.7-slim
LABEL maintainer="Anton Lebedev <mailbox@lebster.me>"
WORKDIR /app
RUN pip install pipenv
RUN pip install gunicorn && pip install gevent
COPY Pipfile* /tmp/
RUN cd /tmp && pipenv lock --requirements > requirements.txt
RUN pip install -r /tmp/requirements.txt
COPY . /app
ENV FLASK_APP=${FLASK_APP}
ENV FLASK_ENV=${FLASK_ENV}
ENV GUNICORN_CMD_ARGS=${GUNICORN_CMD_ARGS}
CMD gunicorn -b ${FLASK_HOST}:${FLASK_PORT} ${GUNICORN_CMD_ARGS} app:app
