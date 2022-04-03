from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('users', include('users.urls')),
    path('books', include('books.urls')),
    #path('/user/login/kakao/callback/', getUserInfo),
    #path('book', include('book.urls')),
    #path('like', include('like.urls')),
]
