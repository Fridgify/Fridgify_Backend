from django.urls import path, include

from Fridgify_Backend.views.fridge.item import item

urlpatterns = [
    # GET
    path('', item.entry_point),
]
