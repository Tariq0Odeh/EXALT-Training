from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions, status
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import (PostSerializer, PostListSerializer,
                          PostDeleteSerializer, CommentSerializer,
                          CommentListSerializer)
from .models import Post, Comment
from django.contrib.auth import get_user_model
User = get_user_model()


class CreatePostView(generics.CreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class DeletePostView(generics.DestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostDeleteSerializer


class EditPostView(generics.UpdateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer


class LargeResultsSetPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 5


class ListPostView(generics.ListAPIView): # Need to edit after make friends feature
    queryset = Post.objects.all()
    serializer_class = PostListSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = LargeResultsSetPagination

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class CreateCommentView(generics.CreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        post_id = self.request.data.get('post_id')
        post = get_object_or_404(Post, id=post_id)
        serializer.save(user=self.request.user, post=post)


class EditCommentView(generics.UpdateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer


class ListCommentView(generics.CreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentListSerializer

    def post(self, request):
        serializer = CommentListSerializer(data=request.data)
        if serializer.is_valid():
            post_id = serializer.validated_data.get('post_id')
            post = get_object_or_404(Post, id=post_id)
            comments = Comment.objects.filter(post=post)
            serialized_comments = CommentSerializer(comments, many=True)
            return Response(serialized_comments.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# return Response({"Heereee"}, status=status.HTTP_200_OK)

# class ListCommentView(generics.ListAPIView):
#     post = get_object_or_404(Post, id=post_id)
#     queryset = Comment.objects.all()
#     serializer_class = CommentSerializer
#     permission_classes = [IsAuthenticatedOrReadOnly]
#     pagination_class = LargeResultsSetPagination
#
#     def perform_create(self, serializer):
#         serializer.save(user=self.request.user)
