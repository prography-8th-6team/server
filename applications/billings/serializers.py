from moneyed import Money
from rest_framework import serializers

from applications.billings.models import Settlement, Billing
from applications.travels.models import Member
from applications.users.models import User


class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = (
            'id',
            'nickname',
        )


class SettlementSerializer(serializers.ModelSerializer):
    member = MemberSerializer(read_only=True)

    class Meta:
        model = Settlement
        fields = (
            'id',
            'member',
            'total_amount',
            'captured_amount',
        )


class BillingSerializer(serializers.ModelSerializer):
    participants = serializers.SerializerMethodField()

    class Meta:
        model = Billing
        fields = (
            'id',
            'travel',
            'title',
            'category',
            'paid_by',
            'paid_date',
            'total_amount',
            'total_amount_currency',
            'captured_amount',
            'participants',
        )

    def __init__(self, *args, **kwargs):
        settlements = kwargs.pop('settlements', None)
        currency = kwargs.pop('currency', None)
        super().__init__(*args, **kwargs)
        self.settlements_data = settlements
        self.currency = currency

    def create(self, validated_data):
        billing = Billing.objects.create(**validated_data)
        for settlement_data in self.settlements_data:
            user_id = settlement_data.get('user')
            member = User.objects.get(travels__members=user_id, travels=billing.travel)
            amount = settlement_data.get('amount')
            currency = self.currency if self.currency else 'USD'
            money = Money(amount, currency)
            Settlement.objects.create(billing=billing, user=member, total_amount=money)
            billing.total_amount += Money(amount, billing.total_amount_currency)
            billing.save(update_fields=['total_amount'])
        return billing

    def get_participants(self, obj):
        settlements = obj.settlements.all()
        members = settlements.values_list('user__nickname', flat=True)
        return members

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        paid_by = representation.get('paid_by')
        if paid_by:
            representation['paid_by'] = instance.paid_by.nickname
        return representation
