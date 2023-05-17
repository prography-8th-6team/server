
# Create your views here.
from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from applications.base.jwt import generate_jwt
from applications.cert.models import User
from applications.cert.utils import kakaoGetUserInfo


class UserViewSet(ModelViewSet):
    queryset = User
    # serializer_class = UserSerializer

    @action(methods=["POST"], detail=False)
    def join(self, request):
        """
        카카오 로그인 시 진입하는 API입니다.
        Client AccessToken 전달 -> 카카오 API -> 정보 저장 후 -> Client JWT Token 전달
        """
        data = request.data.copy()
        ssaid = data.get('ssaid')
        fcm_token = data.get('fcm_token')
        access_token = data.get('access_token')

        kakaoId, nickname = kakaoGetUserInfo(access_token)

        try:
            # TODO : 이미 있는 유저들 토큰 받아서 다시 넘겨주기 ?
            # 이미 있는 애들은 Header에 넘겨주나?
            user = User.objects.get(socialID=kakaoId)
        except User.DoesNotExist as e:
            user = User.objects.create(
                nickname=nickname,
                socialID=kakaoId,
                fcm_token=fcm_token,
                ssaid=ssaid,
            )
        token = generate_jwt(user.id)

        results = {"token": token}
        data_response = {
            "message": "OPERATION_SUCCESS",
            "results": results
        }

        return Response(data_response)
