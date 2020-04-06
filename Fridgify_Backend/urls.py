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
    1. Import the include() function: from django.api_urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.api_urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

from Fridgify_Backend import view

from Fridgify_Backend.api_urls.authentication import auth_urls
from Fridgify_Backend.api_urls.fridge import fridge_urls
from Fridgify_Backend.api_urls.stores import stores_urls


schema_view = get_schema_view(
    openapi.Info(
        title="Fridgify API",
        default_version="v1",
        description="API documentation for Fridgify",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    #  Documentation
    path('', schema_view.with_ui('swagger', cache_timeout=0)),
    #  Authentication Endpoint
    path('auth/', include(auth_urls)),
    #  Fridge Endpoint
    path('fridge/', include(fridge_urls)),
    #  Stores Endpoint
    path('stores/', include(stores_urls)),
    #  Admin Page - can be removed, keeping it just for the lols right now
    #  path('admin/', admin.site.urls),
]
