import json
import bcrypt
import datetime
from django.db import DatabaseError

from Fridgify_Backend.models.users import Users


def register(request):
    req_body = json.loads(request.body)
    if not check_body(req_body):
        return 0
    if Users.objects.filter(username=req_body["username"]).exists():
        return -2
    if Users.objects.filter(email=req_body["email"]):
        return -3
    try:
        Users.objects.create(username=req_body["username"], email=req_body["email"],
                             password=bcrypt.hashpw(req_body["password"].encode("utf-8"),
                                                    bcrypt.gensalt()).decode("utf-8"),
                             name=req_body["name"], surname=req_body["surname"],
                             birth_date=datetime.datetime.strptime(req_body["birthdate"], "%Y-%m-%d"))
    except DatabaseError:
        return -1
    return 1


def check_body(req_body):
    if all(x in req_body for x in ["username", "name", "surname", "email", "password", "birthdate"]):
        return True
    return False
