from django.urls import path

from Fridgify_Backend.views.messaging import register

urlpatterns = [
    # Register Client Token for Messaging Services
    path('register/', register.register_view),
]
