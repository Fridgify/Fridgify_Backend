FROM python:3.7.4-buster

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

EXPOSE 9000

CMD [ "python", "manage.py", "makemigrations", "Fridgify_Backend", "--settings=Fridgify_Backend.settings.production" ]
CMD [ "python", "manage.py", "migrate", "Fridgify_Backend", "--settings=Fridgify_Backend.settings.production" ]
# Beware. It seems like runserver should not be used in production. We should setup some kind of WSGI?
CMD [ "python", "manage.py", "runserver", "0.0.0.0:9000", "--settings=Fridgify_Backend.settings.production" ]
