from friendship.models import Friend
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView
from friendship.models import FriendshipRequest
from friends.serializers import (FriendshipRequestSerializer,
                                 PkRequestSerializer, FriendSerializer)
from django.contrib.auth import get_user_model
User = get_user_model()


class CustomPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 5


class SendRequestView(APIView):
    def post(self, request):
        serializer = PkRequestSerializer(data=request.data)
        if serializer.is_valid():
            try:
                pk = serializer.validated_data.get('pk')
                other_user = User.objects.get(pk=pk)
                Friend.objects.add_friend(
                    request.user,  # The sender
                    other_user,    # The recipient
                    message='Hi! I would like to add you'
                )
                return Response({"Friend request sent successfully."},
                                status=status.HTTP_201_CREATED)
            except User.DoesNotExist:
                return Response({"Recipient user not found."},
                                status=status.HTTP_404_NOT_FOUND)
            except Exception as e:
                return Response({str(e)},
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AcceptRequestView(APIView):
    def get(self, request, pk):
        try:
            friend_request = (FriendshipRequest.objects.get
                              (pk=pk, to_user=request.user))
            friend_request.accept()
            return Response({"Friend request accepted successfully."},
                            status=status.HTTP_200_OK)
        except FriendshipRequest.DoesNotExist:
            return Response({"Friend request not found."},
                            status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({str(e)},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ListRequestsView(APIView):
    pagination_class = CustomPagination
    def get(self, request):
        requests = Friend.objects.unread_requests(user=request.user)
        serializer = FriendshipRequestSerializer(requests, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ListFriendsView(APIView):
    pagination_class = CustomPagination
    def get(self, request):
        requests = Friend.objects.friends(user=request.user)
        serializer = FriendSerializer(requests, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class DeleteFriendView(APIView):
    def delete(self, request):
        serializer = PkRequestSerializer(data=request.data)
        if serializer.is_valid():
            try:
                pk = serializer.validated_data.get('pk')
                other_user = User.objects.get(pk=pk)
                Friend.objects.remove_friend(request.user, other_user)
                return Response({"Friend removed successfully."},
                                status=status.HTTP_204_NO_CONTENT)
            except User.DoesNotExist:
                return Response({"Friend user not found."},
                                status=status.HTTP_404_NOT_FOUND)
            except Exception as e:
                return Response({str(e)},
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)


class MutualFriendsView(APIView):
    pagination_class = CustomPagination
    def post(self, request):
        serializer = PkRequestSerializer(data=request.data)
        if serializer.is_valid():
            try:
                pk = serializer.validated_data.get('pk')
                other_user = User.objects.get(pk=pk)
                user_friends = Friend.objects.friends(request.user)
                other_user_friends = Friend.objects.friends(other_user)
                mutual_friends_set = (set(user_friends)
                                      & set(other_user_friends))
                mutual_friends_data = FriendSerializer(mutual_friends_set,
                                                       many=True).data
                return Response(mutual_friends_data, status=status.HTTP_200_OK)
            except User.DoesNotExist:
                return Response({"error": "User not found."},
                                status=status.HTTP_404_NOT_FOUND)
            except Exception as e:
                return Response({"error": str(e)},
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)
