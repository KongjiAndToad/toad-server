from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', include('user.urls')),
    path('book', include('book.urls')),
    #path('/user/login/kakao/callback/', getUserInfo),
    #path('book', include('book.urls')),
    #path('like', include('like.urls')),
]
