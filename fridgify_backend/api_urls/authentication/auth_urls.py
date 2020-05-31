"""
Routes for authentication views
"""

from django.urls import path

from fridgify_backend.views.authentication import login
from fridgify_backend.views.authentication import register
from fridgify_backend.views.authentication import token

urlpatterns = [
    # POST
    path('register/', register.register_view),
    # POST
    path('login/', login.login_view),
    # GET
    path('token/', token.token_view)
]
