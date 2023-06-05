from django.utils import dateformat
from rest_framework import serializers

from applications.users.models import User


class UserSerializer(serializers.ModelSerializer):
    nickname = serializers.CharField(required=False)
    created = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = ('nickname', 'fcm_token', 'created')

    def get_created(self, obj):
        return dateformat.format(obj.created, 'Y-m-d')
