from rest_framework.views import APIView
from .serializers import UserSerializer, ChangePasswordSerializer, DeactivateSerializer
from rest_framework.response import Response
from rest_framework import status, permissions


class RegisterView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class ChangePasswordView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def put(self, request):
        if request.method == 'PUT':
            serializer = ChangePasswordSerializer(data=request.data)
            if serializer.is_valid():
                user = request.user
                if user.check_password(serializer.data.get('old_password')):
                    user.set_password(serializer.data.get('new_password'))
                    user.save()
                    return Response(
                        {'message': 'Password changed successfully.'},
                        status=status.HTTP_200_OK)
                return Response({'error': 'Incorrect old password.'},
                                status=status.HTTP_400_BAD_REQUEST)
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)


class DeactivateView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request):
        if request.method == 'GET':
            serializer = DeactivateSerializer(data=request.data)
            if serializer.is_valid():
                user = request.user
                user.is_active = False
                user.save()
                return Response({'message': 'Deactivate successfully.'},
                                status=status.HTTP_200_OK)
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)
