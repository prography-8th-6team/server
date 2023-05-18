from datetime import datetime
from datetime import timedelta

import jwt

from config.settings.develop import SECRET_KEY

"""
xxxxx.yyyyy.zzzzz

xxxxx - header (JWT 메타정보) -> token 타입 정의 및 signing 알고리즘
yyyyy - payload -> 토큰 만료 시간, 유저 정보 등 실질적인 데이터
zzzzz - signature -> 인코딩 된 header, payload 그리고 secret key
"""

# TODO : JWT 받고 난 이후 예외처리
# 1. 토큰 없을 떄
# 2. 토큰 만료됐을 때
# 3. 이상한 토큰 왔을 때 (현재 저장되어 있지 않은 토큰일 때)
# 4. 또 뭐있지


def generate_jwt(user_id):
    """
    jwt 신규 발급하는 함수입니다.
    """

    print("=============== generate_jwt start ==============")
    iat = datetime.now()
    print(iat)
    print(iat + timedelta(weeks=2))
    print(iat.timestamp())
    payload = {
        "user_id": user_id,
        "expired": iat + timedelta(weeks=2),
        "iat": iat.timestamp(),
    }
    print("=============== generate_jwt end ==============")

    # return jwt.encode(payload, SECRET_KEY, 'HS256')
    return 11111


def decode_jwt(token):
    return jwt.decode(token, SECRET_KEY, 'HS256')
