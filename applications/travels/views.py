from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema, no_body
from rest_framework import mixins, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from applications.base.response import operation_failure, not_found_data, delete_success, permission_error, \
    invalid_date_range
from applications.base.swaggers import billing_create_api_body, authorizaion_parameters
from applications.billings.serializers import BillingSerializer, MemberSerializer
from applications.travels.models import Travel
from applications.travels.serializers import TravelSerializer
from applications.travels.utils import check_date_order


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
                'title': openapi.Schema(type=openapi.TYPE_INTEGER),
                'start_date': openapi.Schema(type=openapi.FORMAT_DATE),
                'end_date': openapi.Schema(type=openapi.FORMAT_DATE),
                'color': openapi.Schema(type=openapi.TYPE_STRING),
                'description': openapi.Schema(type=openapi.TYPE_STRING),
                'currency': openapi.Schema(type=openapi.TYPE_STRING),
            },
            required=['title', 'color', 'currency', 'start_date', 'end_date'],
        ),
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
                'title': openapi.Schema(type=openapi.TYPE_INTEGER),
                'start_date': openapi.Schema(type=openapi.FORMAT_DATE),
                'end_date': openapi.Schema(type=openapi.FORMAT_DATE),
                'color': openapi.Schema(type=openapi.TYPE_STRING),
                'description': openapi.Schema(type=openapi.TYPE_STRING),
                'currency': openapi.Schema(type=openapi.TYPE_STRING),
            },
        ),
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
