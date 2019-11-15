from django.urls import path, include

from Fridgify_Backend.views.fridge.management import management
from Fridgify_Backend.views.fridge.management import create_fridge
from Fridgify_Backend.views.fridge.management import delete_fridge
from Fridgify_Backend.views.fridge.management import join_fridge

urlpatterns = [
    # POST
    path('', management.entry_point),
    # POST
    path('join/', join_fridge.entry_point),
    # POST
    path('create/', create_fridge.entry_point),
    # DELETE
    path('<int:fridge_id>/', delete_fridge.entry_point),
]
