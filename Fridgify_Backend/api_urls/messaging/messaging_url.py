from django.urls import path

from Fridgify_Backend.views.messaging import register, subscribe

urlpatterns = [
    # Register Client Token for Messaging Services
    path('register/', register.register_view),
    # Subscribe to a Messaging Service
    path('subscribe/', subscribe.subscribe_view),
]
