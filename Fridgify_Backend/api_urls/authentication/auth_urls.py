from django.urls import path, include

from Fridgify_Backend.views.authentication import login
from Fridgify_Backend.views.authentication import register
from Fridgify_Backend.views.authentication import token
from Fridgify_Backend.utils.init_dummy_user import create_dummyuser

urlpatterns = [
    # POST
    path('register/', register.entry_point),
    # POST
    path('login/', login.entry_point),
    # GET
    path('token/', token.entry_point),
    # INFO Temporary for dummy users
    path('dummy/', create_dummyuser)

]
