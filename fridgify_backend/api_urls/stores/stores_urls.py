from django.urls import path

from fridgify_backend.views.stores import stores

urlpatterns = [
    # GET, POST
    path('', stores.stores_view),
]
