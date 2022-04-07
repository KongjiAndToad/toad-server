import json
from django.http.response import JsonResponse
from django.shortcuts import get_object_or_404
from django.views import View
from django.db.models import Q
from users.decorators import login_decorator
import requests, os

from django.shortcuts import render, redirect

from .models import Book
from users.models import User

'''
from text_processor import process_text
from synthesys import SAMPLING_RATE
from synthesys import generate_audio_glow_tts
from io import BytesIO
import scipy.io.wavfile as swavfile
from translate import translate
'''




class BookListView(View):
    # 내 서재 전체 조회
#    @login_decorator
    def get(self, request):
        #user = request.user.id
        #SORT = request.GET.get('sort', '')

        #books = Book.objects.all().filter(user=user).order_by(SORT)
        books = Book.objects.all()

        book_list = [{
            "book_id": book.id,
            "title": book.title,
            #"user_id": book.user.id,
            #"liked_count": book.liked_count
        } for book in books]

        return JsonResponse({"RESULT": book_list}, status=200)

    # 새로운 책 생성
    '''
#    @login_decorator
    def post(self, request):
        data = json.loads(request.body)

        #user = request.user.id
        #title = request.POST['title']
        #txt = request.POST['content']

        title = data.get('title')
        txt = data.get('txt')
        #liked_count = 0

        # 기계 번역
        content = translate(txt)

        # 음성 합성
        text = process_text(content)
        wav = BytesIO()
        try:
            audio = generate_audio_glow_tts(text)
            swavfile.write(wav, rate=SAMPLING_RATE, data=audio.numpy())

        except Exception as e:
            return JsonResponse({"MESSAGE": "음성을 합성할 수 없습니다.: {str(e)}"}, status=500)

        # TODO : S3에 오디오 업로드
        # send_file(wav, mimetype="audio/wave", attachment_filename="audio.wav")

        book = Book(
            title=title,
            content=content,
            #user=user,
            #liked_count=liked_count,
            audio=audio,
        )
        book.save()
        return redirect('/users')
'''


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