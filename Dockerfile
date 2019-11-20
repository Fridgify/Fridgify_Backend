FROM python:3.7.4-buster

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN mkdir /fridgify

WORKDIR /fridgify

RUN pip install pipenv
COPY Pipfile Pipfile.lock /fridgify/
RUN pipenv install --system

ADD . /fridgify/

EXPOSE 9000

CMD bash ./start_server_production.sh
