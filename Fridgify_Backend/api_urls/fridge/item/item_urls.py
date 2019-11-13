from django.urls import path, include

from Fridgify_Backend import view

urlpatterns = [
    # GET
    path('', view.hello_world),
]
