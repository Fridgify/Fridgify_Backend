"""
Routes for fridge management views
"""

from django.urls import path

from fridgify_backend.views.fridge.management import (
    edit_fridge,
    join_fridge,
    create_fridge,
    delete_fridge,
    users,
    qr_code
)


#  /fridge/management/
urlpatterns = [
    #  PATCH
    path('', edit_fridge.edit_fridge_view),
    #  POST
    path('join/', join_fridge.join_view),
    #  POST
    path('create/', create_fridge.create_fridge_view),
    #  DELETE
    path('<int:fridge_id>/', delete_fridge.delete_fridge_view),
    #  GET fridge members
    path('<int:fridge_id>/users', users.fridge_users_view),
    #  PATCH role of fridge members
    path('<int:fridge_id>/users/<int:user_id>/', users.user_role_view),
    #  GET invitation link of fridge (QR-Code)
    path('<int:fridge_id>/qr-code/', qr_code.gen_code_view),
]
