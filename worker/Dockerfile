FROM python:3.7-alpine
LABEL maintainer="Anton Lebedev <mailbox@lebster.me>"
WORKDIR /app
RUN apk add --no-cache ffmpeg
RUN pip install pipenv
COPY Pipfile* /tmp/
RUN cd /tmp && pipenv lock --requirements > requirements.txt
RUN pip install -r /tmp/requirements.txt
COPY . /app
CMD python app.py
