from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema, no_body
from rest_framework import status, mixins
from rest_framework.decorators import action, api_view
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from applications.base.jwt_utils import generate_access_jwt, generate_refresh_jwt
from applications.base.response import certification_failure, not_found_data, delete_success, same_data_failure
from applications.users.models import User
from applications.users.serializers import UserSerializer
from applications.users.utils import kakao_get_user_info, token_equality_check


class UserViewSet(mixins.RetrieveModelMixin,
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
            message = 'LOGIN_SUCCESSFUL'
            status_code = status.HTTP_200_OK

        except User.DoesNotExist:
            user = User.objects.create(
                nickname=kakao_info["nickname"],
                social_id=kakao_info["id"],
                fcm_token=fcm_token,
            )
            message = 'REGISTRATION_SUCCESSFUL'
            status_code = status.HTTP_201_CREATED

        access_token = generate_access_jwt(user.id)
        refresh_token = generate_refresh_jwt(user.id)

        results = {"token": access_token, "refresh_token": refresh_token}
        data_response = {
            "message": message,
            "results": results
        }

        return Response(data_response, status=status_code)

    def get_object(self, pk):
        try:
            return User.objects.get(id=pk)
        except User.DoesNotExist:
            return None

    @swagger_auto_schema(
        operation_summary="유저 개인 프로필 조회 API",
        request_body=no_body,
    )
    def retrieve(self, request, pk, *args, **kwargs):
        user = self.get_object(pk)
        if not user:
            return not_found_data

        user_data = self.serializer_class(user).data
        return Response(user_data)

    @swagger_auto_schema(
        operation_summary="유저 수정 API",
        request_body=no_body,
    )
    def update(self, request, pk):
        user = self.get_object(pk)
        if not user:
            return not_found_data

        serializer = self.serializer_class(user, data=request.data, partial=True)
        if serializer.is_valid():
            updated_travel = serializer.save()
            return Response(self.serializer_class(updated_travel).data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_summary="유저 회원 탈퇴 API",
        request_body=no_body,
    )
    def destroy(self, request, pk):
        user = self.get_object(pk)
        if not user:
            return not_found_data

        user.delete()
        return delete_success


@api_view(["POST"])
def jwt_refresh_token(request):
    data = request.data

    access_token = data.get("access_token", None)
    refresh_token = data.get("refresh_token", None)

    if access_token == refresh_token:
        return same_data_failure

    results = token_equality_check(access_token, refresh_token)
    if not results:
        return certification_failure

    data_response = {
        "message": "operation_success",
        "results": results
    }
    return Response(data_response, status=status.HTTP_200_OK)
