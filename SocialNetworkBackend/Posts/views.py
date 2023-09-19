from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response

# from friends.serializers import FriendSerializer
from .serializers import (CreatePostSerializer, ListPostSerializer,
                          CommentSerializer, LikeSerializer)
from .models import Post, Comment, Like
from django.contrib.auth import get_user_model
User = get_user_model()


class CreatePostView(generics.CreateAPIView):
    queryset = Post.objects.all()
    serializer_class = CreatePostSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ShowEditDeletePostView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = CreatePostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class CustomPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 5


class ListPostCommentsView(generics.ListAPIView):
    serializer_class = CommentSerializer
    pagination_class = CustomPagination

    def get_queryset(self):
        post_id = self.kwargs['pk']
        return Comment.objects.filter(post_id=post_id)


class ListPostView(generics.ListAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = ListPostSerializer
    pagination_class = CustomPagination

    def get_queryset(self):
        user = self.request.user
        friends = user.get_friends()
        friend_ids = [friend.id for friend in friends]
        queryset = Post.objects.filter(user_id__in=friend_ids)
        return queryset


class CreateCommentView(generics.CreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        post_id = self.kwargs['pk']
        post = get_object_or_404(Post, id=post_id)
        serializer.save(user=self.request.user, post=post)


class ShowEditDeleteCommentsView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        post_id = self.kwargs['id']
        comment_id = self.kwargs['pk']
        return Comment.objects.filter(post_id=post_id, id=comment_id)


class CreateLikeView(generics.CreateAPIView):
    serializer_class = LikeSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        post_id = self.kwargs['pk']
        post = get_object_or_404(Post, id=post_id)
        user = self.request.user

        existing_comment = Like.objects.filter(user=user, post=post)
        if existing_comment.exists():
            return Response({"One Like per post"},
                            status=status.HTTP_400_BAD_REQUEST)

        serializer.save(user=user, post=post)


class ShowDeleteLikesView(generics.RetrieveDestroyAPIView):
    serializer_class = LikeSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        post_id = self.kwargs['id']
        like_id = self.kwargs['pk']
        return Like.objects.filter(post_id=post_id, id=like_id)


class ListPostLikesView(generics.ListAPIView):
    serializer_class = LikeSerializer
    pagination_class = CustomPagination

    def get_queryset(self):
        post_id = self.kwargs['pk']
        return Like.objects.filter(post_id=post_id)