from django.urls import path, include

urlpatterns = [
    # GET, POST
    path('<int:fridge_id>/', ),
    # GET, DELETE, POST
    path('<int:fridge_id>/<int:item_id>', ),
]
