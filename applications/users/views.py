from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from applications.base.jwt_utils import generate_jwt
from applications.base.response import certification_failure
from applications.users.models import User
from applications.users.serializers import UserSerializer
from applications.users.utils import kakaoGetUserInfo


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @action(methods=["POST"], detail=False)
    def kakao(self, request):
        """
        카카오 로그인 시 진입하는 API입니다.
        Client AccessToken 전달 -> 카카오 API -> 정보 저장 후 -> Client JWT Token 전달
        """
        data = request.data.copy()

        fcm_token = data.get('fcm_token')
        access_token = data.get('access_token')

        kakao_info = kakaoGetUserInfo(access_token)

        if not kakao_info:
            return certification_failure

        try:
            user = User.objects.get(social_id=kakao_info["id"])
            message = 'login successful'
            status_code = status.HTTP_200_OK

        except User.DoesNotExist:
            user = User.objects.create(
                nickname=kakao_info["nickname"],
                social_id=kakao_info["id"],
                fcm_token=fcm_token,
            )
            message = 'registration successful'
            status_code = status.HTTP_201_CREATED

        token = generate_jwt(user.id)

        results = {"token": token}
        data_response = {
            "message": message,
            "results": results
        }

        return Response(data_response, status=status_code)
