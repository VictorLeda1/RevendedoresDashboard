from django.shortcuts import redirect
from django.contrib.auth import get_user_model
from django.conf import settings
from contas.utils_jwt import decode_jwt
from jwt import InvalidTokenError, ExpiredSignatureError

User = get_user_model()

class JWTAuthenticationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request.user = None
        token = request.COOKIES.get(settings.JWT_COOKIE_NAME)
        if token:
            try:
                payload = decode_jwt(token)
                user = User.objects.filter(pk=payload['uid'],
                                           is_active=True).first()
                request.user = user
            except (InvalidTokenError, ExpiredSignatureError, KeyError):
                # invalida cookie
                response = redirect('/login/')
                response.delete_cookie(settings.JWT_COOKIE_NAME, path='/')
                return response
        return self.get_response(request)