from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema, no_body
from rest_framework import status, mixins
from rest_framework.decorators import action, api_view
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from applications.base.jwt_utils import generate_access_jwt, generate_refresh_jwt
from applications.base.response import certification_failure, not_found_data, delete_success, same_data_failure, \
    operation_failure
from applications.base.swaggers import authorizaion_parameters
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
            200: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'token': openapi.Schema(type=openapi.TYPE_STRING),
                    'refresh_token': openapi.Schema(type=openapi.TYPE_STRING),
                    "user_id": openapi.Schema(type=openapi.TYPE_INTEGER),
                    "nickname": openapi.Schema(type=openapi.TYPE_STRING)
                }
            ),
            401: "CERTIFICATION_FAILURE - 카카오 토큰 인증 오류"
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
        except User.DoesNotExist:
            user = User.objects.create(
                nickname=kakao_info["nickname"],
                social_id=kakao_info["id"],
                fcm_token=fcm_token,
            )

        access_token = generate_access_jwt(user.id)
        refresh_token = generate_refresh_jwt(user.id)

        results = {"token": access_token, "refresh_token": refresh_token, "user_id": user.id, "nickname": user.nickname}
        data_response = {
            "message": "OPERATION_SUCCESS",
            "results": results
        }
        return Response(data_response)

    def get_object(self, pk):
        try:
            return User.objects.get(id=pk)
        except User.DoesNotExist:
            return None

    @swagger_auto_schema(
        operation_summary="유저 개인 프로필 조회 API",
        manual_parameters=[
            authorizaion_parameters
        ],
        responses={
            400: "NOT_FOUND_DATA - 유저를 찾을 수 없는 경우",
        }
    )
    def retrieve(self, request, pk, *args, **kwargs):
        user = self.get_object(pk)
        if not user:
            return not_found_data

        user_data = self.serializer_class(user).data
        results = {
            "message": "OPERATION_SUCCESS",
            "results": user_data
        }
        return Response(results)

    @swagger_auto_schema(
        operation_summary="유저 수정 API",
        manual_parameters=[
            authorizaion_parameters
        ],
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'nickname': openapi.Schema(type=openapi.TYPE_STRING),
                'fcm_token': openapi.Schema(type=openapi.TYPE_STRING),
            },
        ),
        responses={
            400: "NOT_FOUND_DATA - 유저를 찾을 수 없는 경우",
        }
    )
    def update(self, request, pk):
        user = self.get_object(pk)
        if not user:
            return not_found_data

        serializer = self.serializer_class(user, data=request.data, partial=True)
        if serializer.is_valid():
            updated_travel = serializer.save()
            results = {
                "message": "OPERATION_SUCCESS",
                "results": self.serializer_class(updated_travel).data
            }
            return Response(results)
        else:
            return operation_failure

    @swagger_auto_schema(
        operation_summary="유저 회원 탈퇴 API",
        manual_parameters=[
            authorizaion_parameters
        ],
        responses={
            204: "DELETE_SUCCESS - 유저 삭제 성공",
            400: "NOT_FOUND_DATA - 유저를 찾을 수 없는 경우",
        }
    )
    def destroy(self, request, pk):
        user = self.get_object(pk)
        if not user:
            return not_found_data

        user.delete()
        return delete_success


@swagger_auto_schema(
    method='post',
    request_body=openapi.Schema(
        type='object',
        properties={
            'access_token': openapi.Schema(type='string', description='The access token'),
            'refresh_token': openapi.Schema(type='string', description='The refresh token'),
        },
        required=['access_token', 'refresh_token']
    ),
    operation_summary="토큰 재발급 API",
    responses={
        400: "SAME_DATA_FAILURE - access_token과 refresh_token의 값이 동일한 경우",
        401: "CERTIFICATION_FAILURE - JWT 복호화 인증 오류"
    }
)
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
        "message": "OPERATION_SUCCESS",
        "results": results
    }
    return Response(data_response)
