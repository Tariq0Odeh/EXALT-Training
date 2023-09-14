from django.urls import path
from .views import (CreatePostView, ListPostView, DeletePostView, EditPostView
                    , CreateCommentView, EditCommentView, ListCommentView
                    , DeleteCommentView, CreateLikeView, DeleteLikeView
                    , ListLikeView, SinglePostView, SingleCommentView)


urlpatterns = [
    path('create/', CreatePostView.as_view(), name="create-post"),
    path('list/', ListPostView.as_view(), name="list-post"),
    path('<int:pk>/', SinglePostView.as_view(), name="single-post"),
    path('<int:pk>/delete/', DeletePostView.as_view(), name="delete-post"),
    path('<int:pk>/edit/', EditPostView.as_view(), name="edit-post"),
    path('<int:pk>/comments/', ListCommentView.as_view(), name="list-comment"),
    path('create-comment/', CreateCommentView.as_view(), name="create-comment"),
    path('comments/<int:pk>/', SingleCommentView.as_view(),name="edit-comment"),
    path('comments/<int:pk>/edit/', EditCommentView.as_view(),
         name="edit-comment"),
    path('comments/<int:pk>/delete/', DeleteCommentView.as_view(),
         name="delete-comment"),




    path('likes/', CreateLikeView.as_view(), name="create-like-post"),
    path('like/delete/<int:pk>/', DeleteLikeView.as_view(),
         name="delete-like"),
    path('like/list/', ListLikeView.as_view(), name="list-like"),
]
