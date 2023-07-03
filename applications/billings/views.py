from djmoney.money import Money
from drf_yasg.utils import swagger_auto_schema
from rest_framework import mixins, status
from rest_framework.decorators import action, api_view
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from applications.base.swaggers import dispatch_settlement_body, authorizaion_parameters
from applications.billings import SettlementStatus, CurrencyType
from applications.billings.models import Billing, Settlement
from applications.billings.serializers import BillingSerializer


@swagger_auto_schema(
    method='get',
    operation_summary="전체 화폐 리스트 조회 API",
)
@api_view(['GET'])
def get_currencies(request):
    # todo: 섹시한 메서드 있으면 변경
    data_response = {
        "message": "OPERATION_SUCCESS",
        "results": [choice[0] for choice in CurrencyType.CHOICES]
    }
    return Response(data_response)


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
            authorizaion_parameters
        ],
        responses={200: BillingSerializer()}
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="billing 삭제 API",
        manual_parameters=[
            authorizaion_parameters
        ],
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="billing 수정 API",
        manual_parameters=[
            authorizaion_parameters
        ],
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="billing 정산 API",
        manual_parameters=[
            authorizaion_parameters
        ],
        request_body=dispatch_settlement_body,
        responses={200: BillingSerializer()}
    )
    @action(detail=True, methods=['post'])
    def settle(self, request, pk):
        data = request.data.copy()
        user = data.get('user', None)
        amount = data.get('amount', None)
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
        billing.status = SettlementStatus.CHARGED if billing.total_amount - billing.captured_amount == 0 \
            else SettlementStatus.PARTIALLY_CHARGED
        settlement.save(update_fields=['captured_amount', 'status'])
        billing.save(update_fields=['captured_amount', 'status'])
        response_data = {
            'id': pk,
            'travel': billing.travel.pk,
            'title': billing.title,
            'category': billing.category,
            'paid_by': billing.paid_by.nickname,
            'paid_date': billing.paid_date,
            'total_amount': billing.total_amount.amount,
            'captured_amount': billing.captured_amount.amount,
            'total_amount_currency': str(billing.total_amount.currency),
        }
        return Response({'message': 'OPERATION_SUCCESS', 'result': response_data}, status=status.HTTP_200_OK)
