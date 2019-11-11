"""Fridgify_Backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from Fridgify_Backend import view

from Fridgify_Backend.urls.authentication import auth_urls
from Fridgify_Backend.urls.fridge import fridge_urls
from Fridgify_Backend.urls.stores import stores_urls

urlpatterns = [
    # Example View
    path('', view.hello_world, ),
    # Admin Page - can be removed, keeping it just for the lols right now
    path('admin/', admin.site.urls),
    # Authentication Endpoint
    path('auth/', include(auth_urls)),
    # Fridge Endpoint
    path('fridge/', include(fridge_urls)),
    # Stores Endpoint
    path('stores/', include(stores_urls))
]
