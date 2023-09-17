from .models import Post, Comment, Like
from rest_framework import serializers


class CreatePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'title', 'body']


class ListPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'title', 'body', 'user']


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'body']


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ['post_id']


