from rest_framework import generics, permissions, status
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Profile
from .serializers import ProfileSerializer, ProfileUpdateSerializer, ProfileSearchSerializer
from django.contrib.auth import get_user_model
User = get_user_model()

class CreateProfileView(generics.CreateAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class EditProfileView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def put(self, request):
        serializer = ProfileUpdateSerializer(data=request.data)
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


class SearchProfileView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request):
        serializer = ProfileSearchSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            try:
                user = User.objects.get(name=username)
                profile = Profile.objects.get(user=user)
                return Response(ProfileSerializer(profile).data)
            except User.DoesNotExist:
                return Response({'detail': 'User not found.'},
                                status=status.HTTP_404_NOT_FOUND)
            except Profile.DoesNotExist:
                return Response({'detail': 'Profile not found.'},
                                status=status.HTTP_404_NOT_FOUND)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)