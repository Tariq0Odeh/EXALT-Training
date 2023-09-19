from datetime import timezone, datetime

from rest_framework import generics
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.views import APIView
from .models import Story
from .serializer import CreateStorySerializer


class CustomPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 5


class CreatePostView(generics.CreateAPIView):
    queryset = Story.objects.all()
    serializer_class = CreateStorySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ListStoryView(generics.ListAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = CreateStorySerializer
    pagination_class = CustomPagination

    def get_queryset(self):
        user = self.request.user
        friends = user.get_friends()
        friend_ids = [friend.id for friend in friends]
        queryset = Story.objects.filter(user_id__in=friend_ids)
        return queryset


def delete_expired_stories():
    current_time = datetime.now()
    expired_stories = Story.objects.filter(
        expiration_time__lte=current_time)
    expired_stories_count = expired_stories.count()

    if expired_stories_count > 0:
        expired_stories.delete()
        print(
            f'Successfully deleted {expired_stories_count} expired stories.')
    else:
        print('No expired stories to delete.')

