import requests
import jwt
import json

from django.http.response import JsonResponse
from django.views import View
from django.conf import settings

from .models import User

from django.shortcuts import redirect
from toad.config.settings import SOCIAL_OUTH_CONFIG
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny

'''
@api_view(['GET'])
@permission_classes([AllowAny, ])
def kakaoGetLogin(request):
    CLIENT_ID = SOCIAL_OUTH_CONFIG['KAKAO_REST_API_KEY']
    REDIRET_URL = SOCIAL_OUTH_CONFIG['KAKAO_REDIRECT_URI']
    url = "https://kauth.kakao.com/oauth/authorize?response_type=code&client_id={0}&redirect_uri={1}".format(
        CLIENT_ID, REDIRET_URL)
    res = redirect(url)
    return res

@api_view(['GET'])
@permission_classes([AllowAny, ])
def getUserInfo(reqeust):
    CODE = reqeust.query_params['code']
    url = "https://kauth.kakao.com/oauth/token"
    res = {
            'grant_type': 'authorization_code',
            'client_id': SOCIAL_OUTH_CONFIG['KAKAO_REST_API_KEY'],
            'redirect_url': SOCIAL_OUTH_CONFIG['KAKAO_REDIRECT_URI'],
            'client_secret': SOCIAL_OUTH_CONFIG['KAKAO_SECRET_KEY'],
            'code': CODE
        }
    headers = {
        'Content-type': 'application/x-www-form-urlencoded;charset=utf-8'
    }
    response = requests.post(url, data=res, headers=headers)
    # 그 이후 부분
    tokenJson = response.json()
    userUrl = "https://kapi.kakao.com/v2/user/me" # 유저 정보 조회하는 uri
    auth = "Bearer "+tokenJson['access_token'] ## 'Bearer '여기에서 띄어쓰기 필수!!
    HEADER = {
        "Authorization": auth,
        "Content-type": "application/x-www-form-urlencoded;charset=utf-8"
    }
    res = requests.get(userUrl, headers=HEADER)
    return Response(res.text)
'''