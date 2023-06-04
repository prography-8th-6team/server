from djmoney.money import Money
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import mixins, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from applications.base.swaggers import dispatch_settlement_body
from applications.billings import SettlementStatus
from applications.billings.models import Billing, Settlement
from applications.billings.serializers import BillingSerializer


class BillingViewSet(mixins.RetrieveModelMixin,
                     mixins.DestroyModelMixin,
                     mixins.UpdateModelMixin,
                     GenericViewSet):
    serializer_class = BillingSerializer

    def get_queryset(self):
        if self.action == 'settle':
            pk = self.kwargs['pk']
            return Billing.objects.filter(pk=pk)
        else:
            return Billing.objects.all()

    @swagger_auto_schema(
        operation_summary="billing 상세 API",
        manual_parameters=[
            openapi.Parameter('Authorized', openapi.IN_HEADER, description="accesstoken이 없으면 이용 못합니다.",
                              type=openapi.TYPE_STRING, required=True),
        ]
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="billing 삭제 API",
        manual_parameters=[
            openapi.Parameter('Authorized', openapi.IN_HEADER, description="accesstoken이 없으면 이용 못합니다.",
                              type=openapi.TYPE_STRING, required=True),
        ],
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="billing 수정 API",
        manual_parameters=[
            openapi.Parameter('Authorized', openapi.IN_HEADER, description="accesstoken이 없으면 이용 못합니다.",
                              type=openapi.TYPE_STRING, required=True),
        ],
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="billing 생성 API",
        manual_parameters=[
            openapi.Parameter('Authorized', openapi.IN_HEADER, description="accesstoken이 없으면 이용 못합니다.",
                              type=openapi.TYPE_STRING, required=True),
        ],
        request_body=dispatch_settlement_body,
    )
    @action(detail=True, methods=['post'])
    def settle(self, request, pk):
        data = request.data.copy()
        # serializer 로직 이용하기
        user = data.get('user', None)
        amount = data.get('amount', None)
        # 본인의 것만 정산 가능한건지? 확인이 필요할듯!
        if not user or not amount:
            return Response({'message': 'member와 amount 값이 반드시 포함되어야 합니다.'},
                            status=status.HTTP_400_BAD_REQUEST)
        if amount < 0:
            return Response({'message': 'amount의 값은 0이상만 가능합니다..'},
                            status=status.HTTP_400_BAD_REQUEST)
        billing = self.get_queryset().first()
        settlement = Settlement.objects.filter(billing=billing, user=user).first()
        if not billing or not settlement:
            return Response({'message': '해당하는 정산 데이터가 없습니다.'},
                            status=status.HTTP_404_NOT_FOUND)
        money = Money(amount, billing.total_amount.currency)
        settlement.captured_amount += money
        settlement.status = SettlementStatus.CHARGED if settlement.total_amount - settlement.captured_amount == 0 \
            else SettlementStatus.PARTIALLY_CHARGED
        billing.captured_amount += money
        settlement.save(update_fields=['captured_amount', 'status'])
        billing.save(update_fields=['captured_amount'])
        return Response({'message': 'success'}, status=status.HTTP_200_OK)
