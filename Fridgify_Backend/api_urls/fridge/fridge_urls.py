from django.urls import path, include

from Fridgify_Backend import view

from Fridgify_Backend.api_urls.fridge.content import content_urls
from Fridgify_Backend.api_urls.fridge.item import item_urls
from Fridgify_Backend.api_urls.fridge.management import management_urls

urlpatterns = [
    # GET
    path('', view.hello_world),
    # Content Endpoint
    path('content/', include(content_urls)),
    # Item Endpoint
    path('item/', include(item_urls)),
    # Management Endpoint
    path('management/', include(management_urls)),
]
