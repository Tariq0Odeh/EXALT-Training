from django.urls import path
from .views import CreatePostView, ListStoryView

urlpatterns = [
    path('create/', CreatePostView.as_view(), name='create-story'),
    path('list/', ListStoryView.as_view(), name='list-stories')
  ]