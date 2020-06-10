"""
Routes for fridge content views
"""

from django.urls import path

from fridgify_backend.views.fridge.content import fridge_content
from fridgify_backend.views.fridge.content import fridge_content_item

urlpatterns = [
    # GET, POST
    path('<int:fridge_id>/', fridge_content.fridge_content_view),
    # GET, DELETE, POST
    path('<int:fridge_id>/<str:item_id>', fridge_content_item.fridge_content_item_view),
]
