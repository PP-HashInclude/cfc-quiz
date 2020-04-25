FROM python:2-alpine

COPY ./requirements.txt /app/requirements.txt
COPY ./common/ /app/common/
COPY ./controllers/ /app/controllers/
COPY ./data/ /app/data/
COPY ./repositories/ /app/repositories/
COPY ./static/ /app/static/
COPY ./templates/ /app/templates/

WORKDIR /app

RUN apk --update add python py-pip openssl ca-certificates py-openssl wget bash linux-headers
RUN apk --update add --virtual build-dependencies libffi-dev openssl-dev python-dev py-pip build-base \
  && pip install --upgrade pip \
  && pip install --upgrade pipenv\
  && pip install --upgrade -r /app/requirements.txt\
  && apk del build-dependencies

COPY . /app

ENTRYPOINT [ "python" ]

CMD [ "main.py" ]