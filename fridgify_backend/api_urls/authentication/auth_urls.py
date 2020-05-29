from django.urls import path, include

from fridgify_backend.views.authentication import login
from fridgify_backend.views.authentication import register
from fridgify_backend.views.authentication import token
from fridgify_backend.utils.init_dummy_user import setup_database

urlpatterns = [
    # POST
    path('register/', register.register_view),
    # POST
    path('login/', login.login_view),
    # GET
    path('token/', token.token_view),
    # INFO Temporary for dummy users
    path('dummy/', setup_database)

]
