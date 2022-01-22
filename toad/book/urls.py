from django.urls import path
from book.views import (
    BookListView,
    SearchBookView
)

urlpatterns = [
    path('/user/<int:user_id>', BookListView.as_view()),
    path('/search', SearchBookView.as_view()),
]