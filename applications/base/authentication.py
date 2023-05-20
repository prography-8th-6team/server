from rest_framework.authentication import BaseAuthentication

from applications.base.jwt_utils import decode_jwt
from applications.users.models import User


class JsonWebTokenAuthentication(BaseAuthentication):

    def authenticate(self, request):
        access_token = request.headers.get("Authorization", None)
        if not access_token:
            return None

        auth_type, token = access_token.split(' ')
        payload = decode_jwt(token)
        if auth_type == "Bearer":
            user_id = payload.get("user_id", None)
            try:
                user = User.objects.get(id=user_id)
                return user, None
            except User.DoesNotExist:
                return None
        else:
            return None
