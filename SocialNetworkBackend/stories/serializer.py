from .models import Story
from rest_framework import serializers


class CreateStorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Story
        fields = ['id', 'text', 'image']
