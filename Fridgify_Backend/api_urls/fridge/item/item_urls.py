from django.urls import path, include

from Fridgify_Backend.views.fridge.item import item

urlpatterns = [
    # GET
    path('barcode<str:barcode>&item_id<int:item_id>', item.item_view),
]
