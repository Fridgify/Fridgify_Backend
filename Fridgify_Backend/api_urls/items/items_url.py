from django.urls import path

from Fridgify_Backend.views.items import items

urlpatterns = [
    # GET
    path('', items.items_view),
]
