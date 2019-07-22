FROM python:3.7-alpine as base

FROM base as builder

RUN mkdir /install
WORKDIR /install

RUN apk update

RUN apk add libffi-dev openssl-dev gcc build-base

COPY requirements.txt /requirements.txt
RUN pip3 install -r /requirements.txt

FROM base

COPY --from=builder /usr /usr
COPY . /srv/bot_api

WORKDIR /srv/bot_api
RUN chmod 777 /srv/bot_api
RUN chmod 777 gunicornstart.sh

EXPOSE 8080

CMD ["./gunicornstart.sh"]