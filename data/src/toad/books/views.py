import json
import wave
from urllib.parse import urlparse
import urllib.request as req

from django.http.response import JsonResponse
from django.shortcuts import get_object_or_404
from django.views import View
from django.db.models import Q
from users.decorators import login_decorator
import requests, os
import datetime

from django.shortcuts import render, redirect

from .models import Book
from users.models import User

import io,wave
import uuid
import boto3

from config import settings


'''
from text_processor import process_text
from synthesys import SAMPLING_RATE
from synthesys import generate_audio_glow_tts
from io import BytesIO
import scipy.io.wavfile as swavfile
from translate import translate
'''




class BookListView(View):
    # 서재 전체 조회
    def get(self, request):
        books = Book.objects.all()

        book_list = [{
            "book_id": book.id,
            "title": book.title,
        } for book in books]

        return JsonResponse({"RESULT": book_list}, status=200)



    # 새로운 책 생성
    def post(self, request):
        '''
        s3_client = boto3.client(
            's3',
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY
        )
'''
        data = json.loads(request.body)
        title = data["title"]
        text = data["text"]

        text_process = requests.post(url='https://537e-121-65-255-145.ngrok.io/tts-server/api/process-text', json={'text': text})
        #audio_process = requests.post(url='https://11fd-121-162-241-249.ngrok.io/tts-server/api/process-audio', json={'text': text})

        #d = datetime.datetime.now()
        filename = "./audio/tts-audio"+str(uuid.uuid1()).replace('-','')+".wav"
        with open(filename, "wb") as file:  # open in binary mode
            response = requests.post(url='https://537e-121-65-255-145.ngrok.io/tts-server/api/process-audio', json={'text': text})  # get request
            file.write(response.content)  # write to file

        jsonText = text_process.json()
        strText = str(jsonText)[2:-2]

        Book.objects.create(
            title=title,
            content=strText,
            # audio=file_url,
        )
        return JsonResponse({"title": title, "content": strText}, status=201)
'''
        s3_client.upload_fileobj(
            file,
            "toad-server-bucket",
            filename
        )
        file_url = f"https://s3.ap-northeast-2.amazonaws.com/toad-server-bucket/"+filename

        #URL = 'https://c17d-121-65-255-145.ngrok.io/tts-server/api/process-audio'
        #file = req.get(url, allow_redirects=True)

        #open('facebook.ico', 'wb').write(file.content)
'''




class BookView(View):
    def get(self, request, book_id):
        book = get_object_or_404(Book, pk=book_id)

        return JsonResponse(
            {
                "id" : book.pk,
                "title" : book.title,
                "content" : book.content,
            }, status=200
        )




# 내 서재 내에서 검색
class MyBookSearchView(View):
    #@login_decorator
    def get(self, request):
        #user = request.user.id
        book_title = request.GET.get('title', '')
        SORT = request.GET.get('sort', '')

        books = Book.objects.filter(user=user)

        if book_title:
            if len(book_title) > 1:
                books = books.filter(title__icontains=book_title).order_by(SORT)
            else:
                return JsonResponse({"MESSAGE": "검색어는 2글자 이상 입력해주세요"}, status=400)
        if not books:
            return JsonResponse({"RESULT": []}, status=200)

        books_list = [{
            "book_id": book.id,
            "title": book.title,
            #"user_id": book.user.id,
            #"liked_count": book.liked_count,
        } for book in books]

        return JsonResponse({
            "RESULT": books_list,
            "books_count": len(books)
        }, status=200)


# 전체 책에서 검색
class SearchBookView(View):
    def get(self, request):
        book_title = request.GET.get('title', '')
        # SORT = request.GET.get('sort', '')

        if book_title:
            if len(book_title) > 1:
                # books = Book.objects.filter(title__icontains=book_title).order_by(SORT)
                books = Book.objects.filter(title__icontains=book_title)
            else:
                return JsonResponse({"MESSAGE": "검색어는 2글자 이상 입력해주세요"}, status=400)
        if not books:
            return JsonResponse({"RESULT": []}, status=200)

        books_list = [{
            "book_id": book.id,
            "title": book.title,
            # "user_id": book.user.id,
            # "liked_count": book.liked_count,
        } for book in books]

        return JsonResponse({
            "RESULT": books_list,
            "books_count": len(books)
        }, status=200)

class LikeView(View):
    @login_decorator
    def post(self, request, book_id):
        book = get_object_or_404(Book, pk=book_id)
        user = request.user

        if user in book.likes.all():
            book.likes.remove(user)
            book.liked_count = book.likes.count()
            message = "좋아요 취소"
            book.save()
        else:
            book.likes.add(user)
            book.liked_count = book.likes.count()
            message = "좋아요"
            book.save()

        return JsonResponse({
            "book": book.id,
            "user": user.id,
            "liked_count": book.liked_count,
            "message": message
        }, status=200)

    @login_decorator
    def get(self, request):
        SORT = request.GET.get('sort', '')
        user = request.user

        books = user.likes.all()
        if not books:
            return JsonResponse({"RESULT": [], "message": "좋아요한 책이 없습니다."}, status=200)

        books_list = [{
            "book_id": book.id,
            "title": book.title,
            "author": book.user.id,
            "liked_count": book.liked_count,
        } for book in books]

        return JsonResponse({
            "user": user.id,
            "RESULT": books_list,
            "books_count": len(books)
        }, status=200)

class TestView(View):
    def get(self, request):
        response = requests.get(url="http://localhost:8080/todo/1")
        return JsonResponse({
            "content": response.json()
        })

    def post(self, request):

        os.environ['NO_PROXY'] = '127.0.0.1'
        params ={"todoName" : "밥먹기"}

        data = json.loads(request.body)
        todoName = data.get('todoName')
        #txt = data.get('txt')

        r = requests.post(url='http://127.0.0.1:8080/todo/django',  json={'todoName': todoName})
        print("hello")
        print(r)
        print(r.content)
        stringcontent = str(r.content)
        return JsonResponse({
            "name" : stringcontent
        })