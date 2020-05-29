"""
Routes for item views
"""

from django.urls import path

from fridgify_backend.views.items import items, barcode, items_id

urlpatterns = [
    # GET all items
    path('', items.items_view),
    # GET item based on barcode
    path('barcode/<str:barcode>', barcode.barcode_view),
    # GET item based on id
    path('id/<str:item_id>', items_id.id_view),

]
