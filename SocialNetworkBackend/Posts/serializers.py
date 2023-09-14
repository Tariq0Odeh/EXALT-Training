from .models import Post, Comment, Like
from rest_framework import serializers


class CreatePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'title', 'body']


class DeletePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = []


class ListPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'title', 'body', 'user']


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'body']


class CommentListSerializer(serializers.ModelSerializer):
    post_id = serializers.IntegerField()

    class Meta:
        model = Comment
        fields = ['post_id']


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ['post_id']


class ListLikeSerializer(serializers.ModelSerializer):
    post_id = serializers.IntegerField()

    class Meta:
        model = Comment
        fields = ['post_id']


class AllLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ['post_id', 'user', 'post']
