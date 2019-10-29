FROM python:3.7.4-buster

#ADD . /fridgify

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN mkdir /fridgify

WORKDIR /fridgify

COPY requirements.txt /fridgify/

RUN pip install -r requirements.txt

RUN pip install pipenv
COPY Pipfile Pipfile.lock /fridgify/
RUN pipenv install --system

ADD . /fridgify/

#EXPOSE 9000

#CMD [ "python", "./manage.py", "runserver", "localhost:9000" ]
