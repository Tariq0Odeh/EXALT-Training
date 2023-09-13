from django.urls import path
from .views import (CreatePostView, ListPostView, DeletePostView, EditPostView
                    , CreateCommentView, EditCommentView, ListCommentView)


urlpatterns = [
    path('', CreatePostView.as_view(), name="post"),
    path('list/', ListPostView.as_view(), name="list-post"),
    path('delete/<int:pk>/', DeletePostView.as_view(), name="delete-post"),
    path('edit/<int:pk>/', EditPostView.as_view(), name="edit-post"),
    path('comment/', CreateCommentView.as_view(), name="comment-post"),
    path('comment/edit/<int:pk>/', EditCommentView.as_view(), name="edit-comment"),
    path('comment/list/', ListCommentView.as_view(), name="list-comment"),
]
