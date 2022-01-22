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
            "user_id" : book.user.id,
            "liked_count" : book.liked_count
        }for book in books]

        return JsonResponse({"RESULT" : book_list}, status=200)

class SearchBookView(View):
    def get(self, request):
        book_title = request.GET.get('title','')

        if book_title:
            if len(book_title)>1:
                books = Book.objects.filter(title__icontains=book_title).order_by("created_at")
            else:
                return JsonResponse({"MESSAGE": "검색어는 2글자 이상 입력해주세요"}, status=404)
        if not books:
            return JsonResponse({"RESULT": []}, status=200)

        books_list = [{
            "book_num": book.book_num,
            "title" : book.title,
            "user_id" : book.user.id,
            "liked_count" : book.liked_count,
        }for book in books]

        return JsonResponse({
            "RESULT" : books_list,
            "books_count" : len(books)
        }, status=200)