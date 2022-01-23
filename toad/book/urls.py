from django.urls import path
from book.views import (
    BookListView,
    SearchBookView,
    MyBookSearchView,
)

urlpatterns = [
    path('/user/<int:user_id>', BookListView.as_view()),
    path('/search', SearchBookView.as_view()),
    path('/user/<int:user_id>/search', MyBookSearchView.as_view()),
]