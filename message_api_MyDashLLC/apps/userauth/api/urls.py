from django.contrib import admin
from django.urls import path, include

from .views import (
    RegistrationApiView, LoginApiView
)

auth_api_urls = [
    path('register/', RegistrationApiView.as_view(), name='register'),
    path('login/', LoginApiView().as_view(), name='login'),

]


urlpatterns = [
    path('', include(auth_api_urls)),
]