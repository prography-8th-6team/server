from datetime import datetime
from datetime import timedelta

import jwt

from django.conf import settings


def generate_access_jwt(user_id):
    iat = datetime.now()
    expired_date = iat + timedelta(weeks=2)

    payload = {
        "user_id": user_id,
        "expired": expired_date.strftime("%Y-%m-%d %H:%M:%S"),
        "iat": iat.timestamp(),
    }

    return jwt.encode(payload, settings.SECRET_KEY, 'HS256')


def generate_refresh_jwt(user_id):
    iat = datetime.now()
    expired_date = iat + timedelta(weeks=4)

    payload = {
        "user_id": user_id,
        "expired": expired_date.strftime("%Y-%m-%d %H:%M:%S"),
        "iat": iat.timestamp(),
    }

    return jwt.encode(payload, settings.SECRET_KEY, 'HS256')


def decode_jwt(token):
    try:
        return jwt.decode(token, settings.SECRET_KEY, 'HS256')
    except:
        return None


def check_jwt_expired_date(now_date, expired_date):
    now_date = datetime.strptime(now_date, "%Y-%m-%d %H:%M:%S")
    expired_date = datetime.strptime(expired_date, "%Y-%m-%d %H:%M:%S")

    if expired_date <= now_date:
        return True
    else:
        return False

