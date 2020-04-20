#FROM python:2-alpine
FROM python:3.6

WORKDIR /app

COPY ./requirements.txt ./
COPY ./common/. ./common/
COPY ./controllers/. ./controllers/
COPY ./data/. ./data/
COPY ./repositories/. ./repositories/
COPY ./static/. ./static/
COPY ./templates/. ./templates/

RUN pip3 install -r requirements.txt

#RUN apk --update add python3 py-pip openssl ca-certificates py-openssl wget bash linux-headers
#RUN apk --update add --virtual build-dependencies libffi-dev openssl-dev python3-dev py-pip build-base \
#  && pip3 install --upgrade pip \
#  && pip3 install --upgrade pipenv\
#  && pip3 install --upgrade -r /app/requirements.txt\
#  && apk del build-dependencies

COPY . /app

EXPOSE 5000

ENTRYPOINT [ "python3" ]

CMD [ "main.py" ]