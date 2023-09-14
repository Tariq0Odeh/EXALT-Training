from django.shortcuts import get_object_or_404
from rest_framework import generics, status, permissions
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import (CreatePostSerializer, ListPostSerializer,
                          DeletePostSerializer, CommentSerializer,
                          CommentListSerializer, LikeSerializer,
                          ListLikeSerializer, AllLikeSerializer)
from .models import Post, Comment, Like
from django.contrib.auth import get_user_model

User = get_user_model()


class CreatePostView(generics.CreateAPIView):
    queryset = Post.objects.all()
    serializer_class = CreatePostSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class SinglePostView(generics.RetrieveAPIView):
    queryset = Post.objects.all()
    serializer_class = CreatePostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class DeletePostView(generics.DestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = DeletePostSerializer


class EditPostView(generics.UpdateAPIView):
    queryset = Post.objects.all()
    serializer_class = CreatePostSerializer


class CustomPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 5


# -----------------------------------------------------------------------------


class ListPostView(
    generics.ListAPIView):  # Need to edit after make friends feature
    queryset = Post.objects.all()
    serializer_class = ListPostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = CustomPagination

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


# -----------------------------------------------------------------------------


class CreateCommentView(generics.CreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        post_id = self.request.data.get('post_id')
        post = get_object_or_404(Post, id=post_id)
        serializer.save(user=self.request.user, post=post)


class SingleCommentView(generics.RetrieveAPIView):
    queryset = Comment.objects.all()
    serializer_class = CreatePostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class EditCommentView(generics.UpdateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer


class ListCommentView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentListSerializer
    pagination_class = CustomPagination

    def post(self, request):
        serializer = CommentListSerializer(data=request.data)
        if serializer.is_valid():
            post_id = serializer.validated_data.get('post_id')
            post = get_object_or_404(Post, id=post_id)
            comments = Comment.objects.filter(post=post)
            serialized_comments = CommentSerializer(comments, many=True)
            return self.get_paginated_response(serialized_comments.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DeleteCommentView(generics.DestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer


class CreateLikeView(generics.CreateAPIView):
    serializer_class = LikeSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        post_id = self.request.data.get('post_id')
        post = get_object_or_404(Post, id=post_id)
        user = self.request.user
        existing_like = Like.objects.filter(user=user, post=post).first()
        if existing_like:
            return
        serializer.save(user=user, post=post)


class DeleteLikeView(generics.DestroyAPIView):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer


class ListLikeView(generics.ListAPIView):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer

    def post(self, request):
        serializer = LikeSerializer(data=request.data)
        if serializer.is_valid():
            post_id = serializer.validated_data.get('post_id')
            post = get_object_or_404(Post, id=post_id)
            likes = Like.objects.filter(post=post)
            serialized_likes = AllLikeSerializer(likes, many=True)
            return Response(serialized_likes.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)