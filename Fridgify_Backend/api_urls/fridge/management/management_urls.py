from django.urls import path, include

from Fridgify_Backend.views.fridge.management import edit_fridge, join_fridge, create_fridge, delete_fridge, users

urlpatterns = [
    # PATCH
    path('', edit_fridge.edit_fridge_view),
    # POST
    path('join/', join_fridge.entry_point),
    # POST
    path('create/', create_fridge.create_fridge_view),
    # DELETE
    path('<int:fridge_id>/', delete_fridge.delete_fridge_view),
    # GET fridge members
    path('<int:fridge_id>/users', users.fridge_users_view),
    # PATCH role of fridge members
    path('<int:fridge_id>/users/<int:user_id>/', users.user_role_view),
]
