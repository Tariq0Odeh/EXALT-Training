from rest_framework import serializers
from friendship.models import FriendshipRequest
from django.contrib.auth import get_user_model
User = get_user_model()


class FriendshipRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = FriendshipRequest
        fields = '__all__'


class PkRequestSerializer(serializers.Serializer):
    pk = serializers.IntegerField()


class FriendSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name', 'email']

