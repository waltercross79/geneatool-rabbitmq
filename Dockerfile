FROM python:3.6-alpine

RUN apk update && apk add build-base

#ENV FLASK_APP familytree.py
#ENV FLASK_CONFIG docker

RUN adduser -D admin
USER admin

WORKDIR /home/admin

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt --user

COPY src src

# CMD [ "python", "src/person-update.py" ]
