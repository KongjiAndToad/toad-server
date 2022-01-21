from django.urls import path
from book.views import BookListView
urlpatterns = [
    path('/user/<int:user_id>', BookListView.as_view()),
]