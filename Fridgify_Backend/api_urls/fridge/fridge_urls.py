from django.urls import path, include

from Fridgify_Backend.views.fridge import fridge

from Fridgify_Backend.api_urls.fridge.content import content_urls
from Fridgify_Backend.api_urls.fridge.management import management_urls

urlpatterns = [
    # GET
    path('', fridge.fridge_view),
    # Content Endpoint
    path('content/', include(content_urls)),
    # Management Endpoint
    path('management/', include(management_urls)),
]
