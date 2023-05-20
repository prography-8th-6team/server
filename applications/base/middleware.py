# TODO : JWT 받고 난 이후 예외처리
# 1. 토큰 없을 떄
# 2. 토큰 만료됐을 때
# 3. 이상한 토큰 왔을 때 (현재 저장되어 있지 않은 토큰일 때)
# 4. 또 뭐있지
from rest_framework.exceptions import PermissionDenied

from applications.base.jwt_utils import decode_jwt
from applications.users.models import User


class JsonWebTokenMiddleWare(object):

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if (
            request.path != "/v1/user/auth/"
            and "admin" not in request.path
        ):
            headers = request.headers

            access_token = headers.get("Authorization", None)

            if not access_token:
                raise PermissionDenied()

            payload = decode_jwt(access_token[6:])
            user_id = payload.get("user_id", None)
            if not user_id:
                raise PermissionDenied()

            try:
                User.objects.get(id=user_id)
                response = self.get_response(request)
                return response
            except Exception as e:
                return PermissionDenied()
