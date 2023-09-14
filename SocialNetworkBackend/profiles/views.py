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
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters


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


class SearchProfileView(generics.ListAPIView):
    serializer_class = CreateProfileSerializer
    filter_backends = [filters.SearchFilter]
    permission_classes = [IsAuthenticatedOrReadOnly]
    search_fields = ['bio']

    def get_queryset(self):
        queryset = Profile.objects.all()
        username = self.request.query_params.get('username', None)
        if username is not None:
            queryset = queryset.filter(user__username__icontains=username)
        return queryset