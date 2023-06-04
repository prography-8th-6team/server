from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema, no_body
from rest_framework import mixins, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from applications.base.response import operation_failure, not_found_data, delete_success, permission_error, \
    invalid_date_range
from applications.base.swaggers import billing_create_api_body
from applications.billings.serializers import BillingSerializer
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

    @swagger_auto_schema(
        operation_summary="여행 전체 리스트 API",
        request_body=no_body,
    )
    def get_object(self, pk):
        try:
            return Travel.objects.get(id=pk)
        except Travel.DoesNotExist:
            return None

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="여행 생성 API",
        request_body=no_body,
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
                return Response(serializer.data)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return operation_failure

    @swagger_auto_schema(
        operation_summary="여행 상세 API",
        request_body=no_body,
    )
    def retrieve(self, request, pk, *args, **kwargs):
        travel = self.get_object(pk)
        if not travel:
            return not_found_data

        travel_data = self.serializer_class(travel).data
        return Response(travel_data)

    @swagger_auto_schema(
        operation_summary="여행 수정 API",
        request_body=no_body,
    )
    def update(self, request, pk):
        travel = self.get_object(pk)
        if not travel:
            return not_found_data

        serializer = self.serializer_class(travel, data=request.data, partial=True)
        if serializer.is_valid():
            updated_travel = serializer.save()
            return Response(self.serializer_class(updated_travel).data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_summary="여행 삭제 탈퇴",
        request_body=no_body,
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
            openapi.Parameter('Authorized', openapi.IN_HEADER, description="accesstoken이 없으면 이용 못합니다.",
                              type=openapi.TYPE_STRING, required=True),
        ],
        request_body=billing_create_api_body,
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
