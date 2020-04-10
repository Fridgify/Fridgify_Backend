from django.urls import path

from Fridgify_Backend.views.users import users, fridge_users

urlpatterns = [
    # GET
    path('', users.users_view),
    path('<int:fridge_id>/', fridge_users.fridge_users_view)
]
