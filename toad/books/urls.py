from django.urls import path
from books.views import (
    BookListView,
    SearchBookView,
    MyBookSearchView,
    LikeView,
)

urlpatterns = [
    path('/users', BookListView.as_view()),
    path('/search', SearchBookView.as_view()),
    path('/users/search', MyBookSearchView.as_view()),
    path('/<int:book_id>/likes', LikeView.as_view()),
]