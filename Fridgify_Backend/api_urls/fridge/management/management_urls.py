from django.urls import path, include

from Fridgify_Backend.views.fridge.management import edit_fridge
from Fridgify_Backend.views.fridge.management import create_fridge
from Fridgify_Backend.views.fridge.management import delete_fridge
from Fridgify_Backend.views.fridge.management import join_fridge

urlpatterns = [
    # PATCH
    path('', edit_fridge.edit_fridge_view),
    # POST
    path('join/', join_fridge.entry_point),
    # POST
    path('create/', create_fridge.create_fridge_view),
    # DELETE
    path('<int:fridge_id>/', delete_fridge.delete_fridge_view),
]
