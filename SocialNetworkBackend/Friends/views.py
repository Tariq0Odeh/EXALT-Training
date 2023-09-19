from django.shortcuts import render, get_object_or_404
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import serializers
from Friends.models import FriendRequest
from django.contrib.auth import get_user_model

from Friends.serializers import UserDataSerializer

User = get_user_model()


class SendRequestView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request, pk):
        from_user = request.user
        try:
            to_user = User.objects.get(id=pk)  # Retrieve the user by id
        except User.DoesNotExist:
            return Response('User not found',
                            status=status.HTTP_404_NOT_FOUND)

        friend_request, created = FriendRequest.objects.get_or_create(
            from_user=from_user, to_user=to_user)
        if created:
            return Response('friend request sent',
                            status=status.HTTP_200_OK)
        else:
            return Response('Failed to send friend request',
                            status=status.HTTP_400_BAD_REQUEST)


class AcceptRequestView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request, pk):
        friend_request = FriendRequest.objects.get(id=pk)
        if friend_request.to_user == request.user:
            friend_request.to_user.friends.add(friend_request.from_user)
            friend_request.from_user.friends.add(friend_request.to_user)
            friend_request.delete()
            return Response('friend request accepted',
                            status=status.HTTP_200_OK)
        else:
            return Response('Failed an error happened',
                            status=status.HTTP_400_BAD_REQUEST)


class RemoveFriendView(APIView):

    def delete(self, request, pk):
        user = request.user
        friend = get_object_or_404(User, id=pk)
        if friend in user.friends.all():
            user.friends.remove(friend)
            return Response('Friend removed successfully',
                            status=status.HTTP_204_NO_CONTENT)
        else:
            return Response('Friend not found in your friends list',
                            status=status.HTTP_404_NOT_FOUND)


class ShowFriendsView(APIView):

    def get(self, request):
        user = request.user
        friends = user.get_friends()
        serializer = UserDataSerializer(friends, many=True)
        if friends:
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response('Failed an error happened',
                            status=status.HTTP_400_BAD_REQUEST)


class MutualFriendsView(APIView):

    def get(self, request, pk):
        own_user = request.user
        other_user = User.objects.get(id=pk)
        own_user_friends = own_user.get_friends()
        other_user_friends = other_user.get_friends()
        mutual_friends = own_user_friends.intersection(other_user_friends)
        serializer = UserDataSerializer(mutual_friends, many=True)
        if mutual_friends:
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response('Failed an error happened',
                            status=status.HTTP_400_BAD_REQUEST)
