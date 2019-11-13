from django.urls import path, include

from Fridgify_Backend.views.fridge import fridge

from Fridgify_Backend.api_urls.fridge.content import content_urls
from Fridgify_Backend.api_urls.fridge.item import item_urls
from Fridgify_Backend.api_urls.fridge.management import management_urls

urlpatterns = [
    # GET
    path('', fridge.get_fridges),
    # Content Endpoint
    path('content/', include(content_urls)),
    # Item Endpoint
    path('item/', include(item_urls)),
    # Management Endpoint
    path('management/', include(management_urls)),
]
