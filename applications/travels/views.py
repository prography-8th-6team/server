from collections import defaultdict
from datetime import timedelta

from django.db.models import Sum, ExpressionWrapper
from django.utils import timezone
from djmoney.money import Money
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema, no_body
from rest_framework import mixins, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from applications.base.response import operation_failure, not_found_data, delete_success, permission_error, \
    invalid_date_range
from applications.base.swaggers import billing_create_api_body, authorizaion_parameters
from applications.billings.models import Billing, Settlement
from applications.billings.serializers import BillingSerializer, MemberSerializer
from applications.travels.models import Travel, Invite
from applications.travels.serializers import TravelSerializer
from applications.travels.utils import check_date_order, generate_random_string


class TravelViewSet(mixins.CreateModelMixin,
                    mixins.RetrieveModelMixin,
                    mixins.DestroyModelMixin,
                    mixins.ListModelMixin,
                    GenericViewSet):
    queryset = Travel.objects.all()
    serializer_class = TravelSerializer

    def get_object(self, pk):
        try:
            return Travel.objects.get(id=pk)
        except Travel.DoesNotExist:
            return None

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.action == 'list':
            return queryset.filter(members=self.request.user)
        return queryset

    @swagger_auto_schema(
        operation_summary="여행 전체 리스트 API",
        manual_parameters=[
            authorizaion_parameters
        ],
        request_body=no_body,
    )
    def list(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.queryset, many=True)
        data_response = {
            "message": "OPERATION_SUCCESS",
            "results": serializer.data
        }
        return Response(data_response)

    @swagger_auto_schema(
        operation_summary="여행 생성 API",
        manual_parameters=[
            authorizaion_parameters
        ],
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'title': openapi.Schema(type=openapi.TYPE_STRING),
                'start_date': openapi.Schema(type=openapi.FORMAT_DATE),
                'end_date': openapi.Schema(type=openapi.FORMAT_DATE),
                'color': openapi.Schema(type=openapi.TYPE_STRING),
                'description': openapi.Schema(type=openapi.TYPE_STRING),
                'currency': openapi.Schema(type=openapi.TYPE_STRING),
            },
            required=['title', 'color', 'currency', 'start_date', 'end_date'],
        ),
        responses={
            400: "INVALID_DATE_RANGE - 최종 날짜가 시작 날짜보다 이전인 경우",
        }
    )
    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        start_date = data.get("start_date", None)
        end_date = data.get("end_date", None)

        if start_date and end_date:
            if not check_date_order(start_date, end_date):
                return invalid_date_range

            serializer = self.serializer_class(data=request.data, context={"request": request})
            if serializer.is_valid():
                serializer.save()
                results = {
                    "message": "OPERATION_SUCCESS",
                    "results": serializer.data
                }
                return Response(results)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return operation_failure

    @swagger_auto_schema(
        operation_summary="여행 상세 API",
        manual_parameters=[
            authorizaion_parameters
        ],
        responses={
            400: "NOT_FOUND_DATA - 유저를 찾을 수 없는 경우",
        }
    )
    def retrieve(self, request, pk, *args, **kwargs):
        travel = self.get_object(pk)
        if not travel:
            return not_found_data
        travel_data = self.serializer_class(travel, context={'request': request}).data
        data_response = {
            "message": "OPERATION_SUCCESS",
            "results": travel_data
        }
        return Response(data_response)

    @swagger_auto_schema(
        operation_summary="여행 수정 API",
        manual_parameters=[
            authorizaion_parameters
        ],
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'title': openapi.Schema(type=openapi.TYPE_STRING),
                'start_date': openapi.Schema(type=openapi.FORMAT_DATE),
                'end_date': openapi.Schema(type=openapi.FORMAT_DATE),
                'color': openapi.Schema(type=openapi.TYPE_STRING),
                'description': openapi.Schema(type=openapi.TYPE_STRING),
                'currency': openapi.Schema(type=openapi.TYPE_STRING),
            },
        ),
        responses={
            400: "NOT_FOUND_DATA - 유저를 찾을 수 없는 경우",
        }
    )
    def update(self, request, pk):
        travel = self.get_object(pk)
        if not travel:
            return not_found_data

        serializer = self.serializer_class(travel, data=request.data, partial=True)
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
        operation_summary="여행 삭제 탈퇴",
        manual_parameters=[
            authorizaion_parameters
        ],
        responses={
            204: "삭제 성공",
            400: "NOT_FOUND_DATA - 유저를 찾을 수 없는 경우",
            403: "PERMISSION_ERROR - 요청 유저와 여행 관리자가 다를 경우"
        }
    )
    def destroy(self, request, pk, *args, **kwargs):
        travel = self.get_object(pk)
        if not travel:
            return not_found_data

        if request.user.id == travel.user.id:
            travel.delete()
            return delete_success
        else:
            return permission_error

    @swagger_auto_schema(
        operation_summary="billing 생성 API",
        manual_parameters=[
            authorizaion_parameters
        ],
        request_body=billing_create_api_body,
        responses={201: BillingSerializer(),
                   400: 'Operation Error.'}
    )
    @action(detail=True, methods=['post'])
    def billings(self, request, pk):
        # todo: currency 업데이트하는 부분 default currency와 다를 경우, 변환한 값 total에 저장
        # 중복되는 코드들 utils에서 처리하기
        data = request.data.copy()
        travel = self.get_object(pk)
        if not travel:
            return Response({"message": "travel이 존재하지 않습니다."}, status=status.HTTP_404_NOT_FOUND)
        data['travel'] = travel.pk
        settlements = data.pop('settlements', None)
        currency = data.pop('currency', None)
        currency = currency if currency and travel.currency == currency else travel.currency
        serializer = BillingSerializer(data=data, settlements=settlements, currency=currency)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['get'])
    def members(self, request, pk):
        travel = self.get_object(pk)
        members_list = travel.members.all()
        serializer = MemberSerializer(members_list, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_summary="초대 토큰 생성 api",
        manual_parameters=[
            authorizaion_parameters
        ],
        request_body=no_body,
        responses={200: openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'token': openapi.Schema(type=openapi.TYPE_STRING),
            },
        )}
    )
    @action(detail=True, methods=['post'], url_path='generate-invite-token')
    def generate_invite_token(self, request, pk):
        travel = self.get_object(pk)
        today = timezone.now().date()
        invite = Invite.objects.filter(travel=travel, expiry_date__gte=today).first()

        if invite:
            token = invite.token
        else:
            token = generate_random_string(9)
            expiry_date = today + timedelta(days=7)
            Invite.objects.create(travel=travel, token=token, expiry_date=expiry_date)
        return Response({'message': 'success', 'toekn': token}, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_summary="멤버 승인 api",
        manual_parameters=[
            authorizaion_parameters
        ],
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'token': openapi.Schema(type=openapi.TYPE_STRING),
            },
        ),
        responses={200: 'success',
                   400: '이미 여행에 속해있는 멤버입니다.',
                   400: '유효한 토큰 값이 아닙니다. 다시발급 받아주세요.',
                   400: '이미 여행에 속해있는 멤버입니다.'}
    )
    @action(detail=False, methods=['post'])
    def join(self, request):
        token = request.data.get('token', None)
        if not token:
            return Response({'message': '토큰 값이 누락되어있습니다.'}, status=status.HTTP_400_BAD_REQUEST)

        invite = Invite.objects.filter(token=token, expiry_date__gte=timezone.now().date()).first()
        if not invite:
            return Response({'message': '유효한 토큰 값이 아닙니다. 다시발급 받아주세요.'}, status=status.HTTP_404_NOT_FOUND)

        travel = invite.travel
        if travel.member.filter(user=request.user).exists():
            return Response({'message': '이미 여행에 속해있는 멤버입니다.'}, status=status.HTTP_400_BAD_REQUEST)

        travel.members.add(self.request.user)
        return Response({'message': 'success'}, status=status.HTTP_200_OK)
