import jwt, my_settings

from django.conf import settings
from django.http import JsonResponse

from .models import User

def login_decorator(func):
    def wraper(self, request, *args, **kwargs):
        try:
            access_token = request.headers.get('Authorization', None)
            if not access_token:
                request.user = None
                return func(self, request, *args, **kwargs)

            token = jwt.decode(access_token, my_settings.SECRET['secret'], algorithm='HS256')
            user = User.objects.get(email = token['email'])
            request.user = user

        except jwt.exceptions.DecodeError:
            return JsonResponse({'MESSAGE': 'ENCODE_ERROR'}, status=401)
        except User.DoesNotExist:
            return JsonResponse({'MESSAGE': 'INVALID_USER'}, status=401)
        return func(self, request, *args, **kwargs)
    return wraper