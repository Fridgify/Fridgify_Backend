from django.urls import path, include

from Fridgify_Backend import view
from Fridgify_Backend.views.authentication import login_view

urlpatterns = [
    # POST
    path('register/', view.hello_world),
    # POST
    path('login/', login_view.hello_world),
    # GET
    path('token/', view.hello_world),
]
