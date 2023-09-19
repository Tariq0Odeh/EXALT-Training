from django.urls import path
from .views import (SendRequestView, AcceptRequestView, ShowFriendsView,
                    RemoveFriendView, MutualFriendsView)


urlpatterns = [
    path('<int:pk>/send-request/', SendRequestView.as_view(),
         name="send-request"),
    path('<int:pk>/accept-request/', AcceptRequestView.as_view(),
         name="accept-request"),
    path('<int:pk>/remove-friend/', RemoveFriendView.as_view(),
         name="remove-friend"),
    path('<int:pk>/mutual-friends/', MutualFriendsView.as_view(),
         name="mutual-friends"),
    path('show-friends/', ShowFriendsView.as_view(),
         name="show-friends"),
]
