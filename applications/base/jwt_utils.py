from datetime import datetime
from datetime import timedelta

import jwt

from django.conf import settings


def generate_jwt(user_id):
    """
    jwt 신규 발급하는 함수입니다.
    """
    print("=============== generate_jwt start ==============")
    iat = datetime.now()
    expiredDate = iat + timedelta(weeks=2)

    payload = {
        "user_id": user_id,
        "expired": expiredDate.strftime("%Y-%m-%d %H:%M:%S"),
        "iat": iat.timestamp(),
    }
    print("=============== generate_jwt end ==============")

    return jwt.encode(payload, settings.SECRET_KEY, 'HS256')


def decode_jwt(token):
    """
    암호화 된 jwt 데이터를 복호화하는 함수입니다.
    """
    try:
        return jwt.decode(token, settings.SECRET_KEY, 'HS256')
    except Exception:
        return None
