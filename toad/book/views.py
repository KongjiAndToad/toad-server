import json
from django.http.response import JsonResponse
from django.views import View
from django.db.models import Q

from django.shortcuts import render

from .models import Book
from user.models import User

class BookListView(View):
    def get(self, request, user_id):
        user = User.id

        books = Book.objects.all().filter(user=user_id).order_by("created_at")

        book_list = [{
            "book_num" : book.book_num,
            "title" : book.title,
        }for book in books]

        return JsonResponse({"RESULT" : book_list}, status=200)