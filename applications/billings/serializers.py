from moneyed import Money
from rest_framework import serializers

from applications.billings.models import Settlement, Billing
from applications.travels.models import Member


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
    # paid_by = MemberSerializer(read_only=True)
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
            member_id = settlement_data.get('member')
            member = Member.objects.get(id=member_id)
            amount = settlement_data.get('amount')
            currency = self.currency if self.currency else 'USD'
            money = Money(amount, currency)
            Settlement.objects.create(billing=billing, member=member, total_amount=money)
            billing.total_amount += Money(amount, billing.total_amount_currency)
            billing.save(update_fields=['total_amount'])
        return billing

    def get_participants(self, obj):
        settlements = obj.settlements.all()
        members = settlements.values_list('member', flat=True)
        member_objects = Member.objects.filter(id__in=members)
        serializer = MemberSerializer(member_objects, many=True)
        return serializer.data

# class BillingSerializer(serializers.ModelSerializer):
#     paid_by = MemberSerializer(read_only=True)
#     participants = serializers.SerializerMethodField()
#
#     class Meta:
#         model = Billing
#         fields = (
#             'id',
#             'travel',
#             'title',
#             'category',
#             'paid_by',
#             'paid_date',
#             'total_amount',
#             'total_amount_currency',
#             'captured_amount',
#             'participants',
#         )
#
    def get_participants(self, obj):
        settlements = obj.settlements.all()
        members = settlements.values_list('member', flat=True)
        member_objects = Member.objects.filter(id__in=members)
        serializer = MemberSerializer(member_objects, many=True)
        return serializer.data


