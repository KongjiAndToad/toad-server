from django.urls import path
from books.views import (
    BookListView,
    SearchBookView,
    MyBookSearchView,
)

urlpatterns = [
    path('/users/<int:user_id>', BookListView.as_view()),
    path('/search', SearchBookView.as_view()),
    path('/users/<int:user_id>/search', MyBookSearchView.as_view()),
]