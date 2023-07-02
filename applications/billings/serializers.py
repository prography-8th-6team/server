from moneyed import Money
from rest_framework import serializers

from applications.billings.models import Settlement, Billing, BillingImage
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
    user = MemberSerializer(read_only=True)

    class Meta:
        model = Settlement
        fields = (
            'user',
            'total_amount',
            'captured_amount',
        )


class BillingImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = BillingImage
        fields = ('image',)


class BillingSerializer(serializers.ModelSerializer):
    participants = serializers.SerializerMethodField()
    images = BillingImageSerializer(many=True, required=False)

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
            'images',
            'participants',
        )

    def __init__(self, *args, **kwargs):
        import json
        settlements = kwargs.pop('settlements', '')
        currency = kwargs.pop('currency', None)
        images = kwargs.pop('images', None)
        super().__init__(*args, **kwargs)
        if settlements:
            self.settlements_data = json.loads(settlements[0])
        else:
            self.settlements_data = []
        self.currency = currency
        self.images = images if images else None

    def create(self, validated_data):
        billing = Billing.objects.create(**validated_data)
        for settlement_data in self.settlements_data:
            user_id = settlement_data.get('user')
            member = Member.objects.filter(user__id=user_id, travel=billing.travel).first()
            amount = settlement_data.get('amount')
            currency = self.currency if self.currency else 'USD'
            money = Money(amount, currency)
            Settlement.objects.create(billing=billing, user=member.user, total_amount=money)
            billing.total_amount += Money(amount, billing.total_amount_currency)
            billing.save(update_fields=['total_amount'])
        if self.images:
            for image in self.images:
                BillingImage.objects.create(billing=billing, image=image)
        return billing

    def get_participants(self, obj):
        settlements = obj.settlements.all()
        serializer = SettlementSerializer(settlements, many=True)
        return serializer.data

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        paid_by = representation.get('paid_by')
        if paid_by:
            representation['paid_by'] = instance.paid_by.nickname
        return representation
