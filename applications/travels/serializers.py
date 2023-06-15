from rest_framework import serializers

from applications.billings import CurrencyType
from applications.billings.models import Settlement
from applications.billings.serializers import BillingSerializer
from applications.travels.models import Travel, Member, Invite
from applications.users.models import User


class UserTinySerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['nickname']


class TravelSerializer(serializers.ModelSerializer):
    members = UserTinySerializer(many=True, read_only=True)
    billings = BillingSerializer(many=True, read_only=True)
    my_total_billing = serializers.SerializerMethodField()

    def create(self, validated_data):
        request = self.context["request"]
        data = request.data.copy()

        travel = Travel.objects.create(
            user=request.user,
            title=data.get("title"),
            color=data.get("color"),
            start_date=data.get("start_date"),
            end_date=data.get("end_date"),
            description=data.get("description", None),
            currency=data.get("currency", CurrencyType.USD),
        )

        Member.objects.create(
            user=request.user,
            travel=travel,
            is_admin=True,
        )
        return travel

    def to_representation(self, instance):
        data = super().to_representation(instance)
        member_list = []
        for member in data["members"]:
            member_list.append(member["nickname"])
        data['members'] = member_list
        return data

    class Meta:
        model = Travel
        fields = [
            "id",
            "description",
            "members",
            "title",
            "start_date",
            "end_date",
            "color",
            "currency",
            "total_captured_amount",
            "total_amount",
            'my_total_billing',
            "billings",
        ]

    def get_my_total_billing(self, instance):
        request = self.context.get('request', None)
        if request:
            settlements = Settlement.objects.filter(user=request.user, billing__travel=instance)
            return sum([settlement.total_amount.amount - settlement.captured_amount.amount for settlement in settlements])
        return 0


class InviteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invite
        fields = (
            'id',
            'travel',
            'link',
            'expiry_date',
        )
