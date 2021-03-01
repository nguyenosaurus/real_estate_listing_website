FROM tiangolo/uwsgi-nginx-flask:python3.6-alpine3.7
RUN apk update
RUN apk --update add bash nano
RUN apk add postgresql-dev gcc python3-dev musl-dev
RUN apk add postgresql-client
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
RUN python -m pip install -e .