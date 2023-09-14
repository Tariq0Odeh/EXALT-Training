from rest_framework import generics, permissions, status
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Profile
from .serializers import (CreateProfileSerializer,
                          EditProfileSerializer,
                          SearchProfileSerializer)
from django.contrib.auth import get_user_model
User = get_user_model()


class CreateProfileView(generics.CreateAPIView):
    queryset = Profile.objects.all()
    serializer_class = CreateProfileSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class EditProfileView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def put(self, request):
        serializer = EditProfileSerializer(data=request.data)
        if serializer.is_valid():
            profile = request.user.profile
            profile.bio = serializer.data.get('bio')
            profile.website = serializer.data.get('website')
            profile.image = serializer.data.get('image')
            profile.save()
            return Response(
                {'message': 'Profile edited successfully.'},
                status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SearchProfileView(generics.RetrieveAPIView):
    serializer_class = SearchProfileSerializer

    def get_object(self):
        username = self.request.query_params.get('username')
        if username is None:
            raise Response("Please provide a 'username' query parameter",
                           status=status.HTTP_400_BAD_REQUEST)
        try:
            user = User.objects.get(name=username)
            profile = Profile.objects.get(user=user)
            return profile
        except User.DoesNotExist:
            raise Response("User not found",
                           status=status.HTTP_400_BAD_REQUEST)
