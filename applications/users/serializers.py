from rest_framework import serializers

from applications.users.models import User


class UserSerializer(serializers.ModelSerializer):
    nickname = serializers.CharField(required=False)
    social_id = serializers.CharField(required=False)

    class Meta:
        model = User
        fields = ('nickname', 'fcm_token', 'social_id')
