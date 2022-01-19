from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('user', include('user.urls')),
    path('book', include('book.urls')),
    path('like', include('like.urls')),
]
