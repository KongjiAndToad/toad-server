import json
from django.http.response import JsonResponse
from django.views import View
from django.db.models import Q

from django.shortcuts import render

from .models import Book
from users.models import User

#내 서재 전체 조회
class BookListView(View):
    def get(self, request, user_id):
        user = User.id
        SORT = request.GET.get('sort','')

        books = Book.objects.all().filter(user=user_id).order_by(SORT)

        book_list = [{
            "book_num" : book.book_num,
            "title" : book.title,
            "user_id" : book.user.id,
            "liked_count" : book.liked_count
        }for book in books]

        return JsonResponse({"RESULT" : book_list}, status=200)

#내 서재 내에서 검색
class MyBookSearchView(View):
    def get(self, request, user_id):
        user = User.id
        book_title = request.GET.get('title','')
        SORT = request.GET.get('sort','')

        books = Book.objects.filter(user=user_id)

        if book_title:
            if len(book_title)>1:
                books = books.filter(title__icontains=book_title).order_by(SORT)
            else:
                return JsonResponse({"MESSAGE": "검색어는 2글자 이상 입력해주세요"}, status=404)
        if not books:
            return JsonResponse({"RESULT": []}, status=200)

        books_list = [{
            "book_num": book.book_num,
            "title": book.title,
            "user_id": book.user.id,
            "liked_count": book.liked_count,
        } for book in books]

        return JsonResponse({
            "RESULT": books_list,
            "books_count": len(books)
        }, status=200)

#전체 책에서 검색
class SearchBookView(View):
    def get(self, request):
        book_title = request.GET.get('title','')
        SORT = request.GET.get('sort','')

        if book_title:
            if len(book_title)>1:
                books = Book.objects.filter(title__icontains=book_title).order_by(SORT)
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