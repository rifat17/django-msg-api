from django.contrib import admin
from django.urls import path, include

from .views import (
    MessageApiView,
)

message_api_urls = [
    path('messages/', MessageApiView.as_view(), name='messages'),
]


urlpatterns = [
    path('', include(message_api_urls)),
]