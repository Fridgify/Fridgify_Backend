import json
import bcrypt
import datetime
from Fridgify_Backend.models.users import Users


def check_credentials(request):
    """ Check user credentials passed in the request

    :param request: Request containing "username" and "password"
    :return: Integer, either -1 (invalid request), 0 (wrong credentials), 1 (correct credentials)
    """
    print("Checking credentials...")
    # Get request body as JSON
    req_body = json.loads(request.body)
    # Check if keys are existing
    if "username" not in req_body:
        return -1
    if "password" not in req_body:
        return -1
    # Retrieve the password from database for user
    password = retrieve_password(req_body["username"])
    # Check if password/user exists
    if password is None:
        return 0
    # Check if password is correct
    if bcrypt.checkpw(req_body["password"].encode("utf-8"), password.encode("utf-8")):
        print("Password matches.")
        return 1
    else:
        print("Password does not match.")
        return 0


def retrieve_password(username):
    print("Retrieve password for user from database...")
    # Only one object should be inside of here
    objects = Users.objects.filter(username=username).values()
    if len(objects) > 1:
        print("Something went horribly wrong... There are multiple hits for the given username :(")
    elif len(objects) == 0:
        objects = Users.objects.filter(email=username).values()
    if objects.first() is None:
        return None
    return objects.first()["password"]
