from django.urls import path, include

from Fridgify_Backend import view

urlpatterns = [
    # GET, POST
    path('<int:fridge_id>/', view.hello_world),
    # GET, DELETE, POST
    path('<int:fridge_id>/<int:item_id>', view.hello_world),
]
