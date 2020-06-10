"""
Routes for fridge views
"""

from django.urls import path, include

from fridgify_backend.views.fridge import fridge

from fridgify_backend.api_urls.fridge.content import content_urls
from fridgify_backend.api_urls.fridge.management import management_urls

urlpatterns = [
    # GET
    path('', fridge.fridge_view),
    # Content Endpoint
    path('content/', include(content_urls)),
    # Management Endpoint
    path('management/', include(management_urls)),
]
