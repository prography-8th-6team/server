from rest_framework import serializers

from applications.travel.models import Travel, Member


class TravelSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        print("====== create ======")
        request = self.context["request"]
        data = request.data.copy()

        travel = Travel.objects.create(
            user=request.user,
            title=data.get("title"),
            start_date=data.get("start_date"),
            end_date=data.get("end_date"),
        )
        Member.objects.create(
            user=request.user,
            travel=travel,
            is_admin=True,
        )
        return travel

    class Meta:
        model = Travel
        fields = '__all__'
