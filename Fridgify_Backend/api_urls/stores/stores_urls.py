from django.urls import path

from Fridgify_Backend.views.stores import stores

urlpatterns = [
    # GET, POST
    path('', stores.stores_view),
]
