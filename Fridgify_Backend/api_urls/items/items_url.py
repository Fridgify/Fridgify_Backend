from django.urls import path

from Fridgify_Backend.views.items import items
from Fridgify_Backend.views.items import barcode
from Fridgify_Backend.views.items import id

urlpatterns = [
    # GET all items
    path('', items.items_view),

    # GET item based on barcode
    path('barcode/<str:barcode>', barcode.barcode_view),

    # GET item based on id
    path('id/<str:item_id>', id.id_view),

]
