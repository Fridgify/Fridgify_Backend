from django.urls import path, include

from Fridgify_Backend.views.stores import stores

urlpatterns = [
    # GET, POST
    path('', stores.entry_point),
]
