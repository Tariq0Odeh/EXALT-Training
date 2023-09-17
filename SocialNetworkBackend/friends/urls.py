from django.urls import path
from .views import (SendRequestView, AcceptRequestView, ListRequestsView,
                    ListFriendsView, DeleteFriendView, MutualFriendsView)

urlpatterns = [
    path('send-request/', SendRequestView.as_view(),
         name='send-friend-request'),
    path('accept-request/<int:pk>/', AcceptRequestView.as_view(),
         name='accept-friend-request'),
    path('list-requests/', ListRequestsView.as_view(),
         name='list-friend-request'),
    path('list/', ListFriendsView.as_view(),
         name='list-friend'),
    path('delete/', DeleteFriendView.as_view(),
         name='delete-friend'),
    path('mutual/', MutualFriendsView.as_view(),
         name='mutual-friend'),
]