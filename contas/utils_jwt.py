import jwt, datetime
from django.conf import settings
from django.utils import timezone

def generate_jwt(user):
    now = timezone.now()
    payload = {
        'uid': user.pk,
        'iat': int(now.timestamp()),
        'exp': int((now + settings.JWT_EXP_DELTA).timestamp()),
    }
    return jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.JWT_ALG)

def decode_jwt(token):
    return jwt.decode(token, settings.SECRET_KEY,
                      algorithms=[settings.JWT_ALG])