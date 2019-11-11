from django.urls import path, include

from Fridgify_Backend import view

urlpatterns = [
    # POST
    path('register/', view.hello_world),
    # POST
    path('login/', view.hello_world),
    # GET
    path('token/', view.hello_world),
]
