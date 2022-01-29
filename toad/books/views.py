import json
from django.http.response import JsonResponse
from django.views import View
from django.db.models import Q
from users.decorators import login_decorator

from django.shortcuts import render

from .models import Book
from users.models import User

#내 서재 전체 조회
class BookListView(View):
    @login_decorator
    def get(self, request):
        user = request.user.id
        SORT = request.GET.get('sort','')

        books = Book.objects.all().filter(user=user).order_by(SORT)

        book_list = [{
            "book_id" : book.id,
            "title" : book.title,
            "user_id" : book.user.id,
            "liked_count" : book.liked_count
        }for book in books]

        return JsonResponse({"RESULT" : book_list}, status=200)

#내 서재 내에서 검색
class MyBookSearchView(View):
    @login_decorator
    def get(self, request):
        user = request.user.id
        book_title = request.GET.get('title','')
        SORT = request.GET.get('sort','')

        books = Book.objects.filter(user=user)

        if book_title:
            if len(book_title)>1:
                books = books.filter(title__icontains=book_title).order_by(SORT)
            else:
                return JsonResponse({"MESSAGE": "검색어는 2글자 이상 입력해주세요"}, status=404)
        if not books:
            return JsonResponse({"RESULT": []}, status=200)

        books_list = [{
            "book_id": book.id,
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
            "book_id": book.id,
            "title" : book.title,
            "user_id" : book.user.id,
            "liked_count" : book.liked_count,
        }for book in books]

        return JsonResponse({
            "RESULT" : books_list,
            "books_count" : len(books)
        }, status=200)


class LikeView(View):
    @login_decorator
    def post(self, request, book_id):
        book = Book.objects.get(id=book_id)
        user = request.user

        if user in book.likes.all():
            book.likes.remove(user)
            book.liked_count = book.likes.count()
            message = "좋아요 취소"
        else:
            book.likes.add(user)
            book.liked_count = book.likes.count()
            message = "좋아요"

        return JsonResponse({
            "book" : book.id,
            "user" : user.id,
            "liked_count" : book.liked_count,
            "message" : message
        }, status=200)