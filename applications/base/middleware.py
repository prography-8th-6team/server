from datetime import datetime

from jwt import ExpiredSignatureError
from rest_framework.exceptions import PermissionDenied

from applications.base.jwt_utils import decode_jwt, check_jwt_expired_date
from applications.base.response import authorization_error, expired_token


class JsonWebTokenMiddleWare(object):

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            if (
                request.path != "/v1/users/auth/kakao"
                and request.path != "/v1/refresh_token"
                and "admin" not in request.path
                and "swagger" not in request.path
            ):
                access_token = request.headers.get("Authorization", None)
                if not access_token:
                    raise PermissionDenied()

                auth_type, token = access_token.split(' ')
                if auth_type == "Bearer":
                    payload = decode_jwt(token)
                    if not payload:
                        raise PermissionDenied("permission denied")

                    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    token_expired = payload.get('expired')

                    if check_jwt_expired_date(now, token_expired):
                        raise ExpiredSignatureError()

                    user_id = payload.get("user_id", None)
                    if not user_id:
                        raise PermissionDenied()

                else:
                    raise PermissionDenied()

            response = self.get_response(request)
            return response

        except ValueError:
            return authorization_error

        except PermissionDenied:
            return authorization_error

        except ExpiredSignatureError:
            return expired_token
