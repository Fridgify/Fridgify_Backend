from django.urls import path, include

from Fridgify_Backend import view

urlpatterns = [
    # POST
    path('', view.hello_world),
    # POST
    path('join/', view.hello_world),
    # POST
    path('create/', view.hello_world),
    # DELETE
    path('<int:fridge_id>/', view.hello_world),
]
