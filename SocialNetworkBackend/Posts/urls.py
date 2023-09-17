from django.urls import path
from .views import (CreatePostView, ListPostView, ShowEditDeletePostView
                    , CreateCommentView, ListPostCommentsView
                    , ShowEditDeleteCommentsView, CreateLikeView
                    , ShowDeleteLikesView, ListPostLikesView)


urlpatterns = [
    path('create/', CreatePostView.as_view(),
         name="create-post"),
    path('list/', ListPostView.as_view(),
         name="list-post"),
    path('<int:pk>/', ShowEditDeletePostView.as_view(),
         name="show-edit-delete-post"),
    path('<int:pk>/comments/', ListPostCommentsView.as_view(),
         name="list-comment-post"),
    path('<int:pk>/likes/', ListPostLikesView.as_view(),
         name="list-like-post"),
    path('<int:pk>/create-comment/', CreateCommentView.as_view(),
         name="create-comment"),
    path('<int:id>/comments/<int:pk>/', ShowEditDeleteCommentsView.as_view(),
         name="show-edit-delete-comment"),
    path('<int:pk>/make-like/', CreateLikeView.as_view(),
         name="create-like-post"),
    path('<int:id>/likes/<int:pk>/', ShowDeleteLikesView.as_view(),
         name="show-delete-like"),
]
