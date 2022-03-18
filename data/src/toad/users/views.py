import json, re, traceback, jwt, my_settings

from django.http            import JsonResponse  
from django.views           import View          
from django.core.exceptions import ValidationError
from django.db.models       import Q                                                                                                                
from .models                import User
import bcrypt
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

MINIMUM_PASSWORD_LENGTH = 8  #< -- 비밀번호 최소값을 저장해둔 전역변수

class SignUp(View):
    def post(self, request):
        data =json.loads(request.body)

def validate_email(email):
    pattern = re.compile('^.+@+.+\.+.+$')
    if not pattern.match(email):
        return JsonResponse({'message': 'INVALID_EMAIL'}, status=400)

# 패스워드 길이 검사
def validate_password(password):
    if len(password) < MINIMUM_PASSWORD_LENGTH:
        return JsonResponse({'message': 'SHORT_PASSWORD'}, status=400)

class SignUpView(View):
    def validate_email(email):
        pattern = re.compile('^.+@+.+\.+.+$')
        if not pattern.match(email):
            return JsonResponse({'message': 'INVALID_EMAIL'}, status=400)

    # 패스워드 길이 검사
    def validate_password(password):
        if len(password) < MINIMUM_PASSWORD_LENGTH:
            return JsonResponse({'message': 'SHORT_PASSWORD'}, status=400)

    @method_decorator(csrf_exempt, name='dispatch')
    def post(self, request):
        data = json.loads(request.body)

        try:
            email = data.get('email', None)
            password = data.get('password', None)
            nickname = data.get('nickname', None)

            # KEY_ERROR check
            if not (password and email and nickname):
                return JsonResponse({'message': 'KEY_ERROR'}, status=400)

                # validation check
            pattern = re.compile('^.+@+.+\.+.+$')
            if not pattern.match(email):
                return JsonResponse({'message': 'INVALID_EMAIL'}, status=400)

            if len(password) < MINIMUM_PASSWORD_LENGTH:
                return JsonResponse({'message': 'SHORT_PASSWORD'}, status=400)

            # unique check
            user = User.objects.filter(Q(email=email))
            if not user:
                User.objects.create(
                    email=email,
                    nickname=nickname,
                    password=bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
                )
                return JsonResponse({'message': 'SUCCESS'}, status=200)

            return JsonResponse({'message': 'USER_ALREADY_EXISTS'}, status=409)

        except KeyError:
            return JsonResponse({"message": "KEY_ERROR"}, status=400)

class LoginView(View):
    def post(self, request):
        data = json.loads(request.body)

        try:
            email = data.get('email')
            password = data.get('password')

            if User.objects.filter(Q(email=email)).exists():
                user = User.objects.get(email=email)
                #Password 검사 및 암호화
                if bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
                    token = jwt.encode({'email' : email}, my_settings.SECRET['secret'], algorithm = 'HS256').decode('utf-8')
                    #로그인 성공(200)

                    return JsonResponse({
                        "message":"SUCCESS",
                        "token" : token
                    }, status=200)
                #로그인 실패 - 비밀번호 오류 (401)
                return JsonResponse({"message":"INVALID_PASSWORD"}, status=401)
            #로그인 실패 - 아이디 오류(401)
            return JsonResponse({"message":"INVALID_USER"}, status=401)
        #키 에러(400)
        except KeyError:
            return JsonResponse({"message":"KEY_ERROR"}, status=400)