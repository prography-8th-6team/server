from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema, no_body
from rest_framework import status, mixins
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from applications.base.jwt_utils import generate_jwt
from applications.base.response import certification_failure
from applications.users.models import User
from applications.users.serializers import UserSerializer
from applications.users.utils import kakao_get_user_info


class UserViewSet(mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.DestroyModelMixin,
                  GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @swagger_auto_schema(
        operation_summary="카카오 로그인 API",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'access_token': openapi.Schema(type=openapi.TYPE_STRING),
                'fcm_token': openapi.Schema(type=openapi.TYPE_STRING),
            },
            required=['access_token']
        ),
        responses={
            200: "operation_success",
            401: "certification_failure",
        }
    )
    @action(methods=["POST"], detail=False, url_path="auth/kakao")
    def kakao(self, request):
        """
        카카오 로그인 시 진입하는 API입니다.
        Client AccessToken 전달 -> 카카오 API -> 정보 저장 후 -> Client JWT Token 전달
        """
        data = request.data.copy()

        fcm_token = data.get('fcm_token')
        access_token = data.get('access_token')

        kakao_info = kakao_get_user_info(access_token)

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

    @swagger_auto_schema(
        operation_summary="유저 개인 프로필 조회 API",
        request_body=no_body,
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="유저 수정 API",
        request_body=no_body,
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="유저 회원 탈퇴 API",
        request_body=no_body,
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

