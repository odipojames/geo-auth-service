from django.core.mail import send_mail
from django.conf import settings
from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from .models import Profile
from .serializers import (CustomTokenObtainSerializer, UserSerializer, 
                          ResetPasswordRequestSerializer, PasswordResetConfirmSerializer, ProfileSerializer)
from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from auth.settings import site_url
from drf_yasg.utils import swagger_auto_schema



User = get_user_model()

class RegisterUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

class CustomTokenObtainView(generics.CreateAPIView):
    serializer_class = CustomTokenObtainSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        token_data = serializer.create(serializer.validated_data)
        return Response(token_data, status=status.HTTP_200_OK)
    


@swagger_auto_schema(request_body=ResetPasswordRequestSerializer)
class ResetPasswordRequestView(APIView):
    permission_classes = [AllowAny]
    def post(self, request, *args, **kwargs):
        serializer = ResetPasswordRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        token = serializer.save()

        # Send the token via email
        subject = 'Password Reset Request'
        message = "{}/api/confirm-reset-password/?token={}".format(
            site_url, token
        )
        from_email = settings.EMAIL_HOST_USER
        to_email = serializer.validated_data['email']
        
        try:
            send_mail(subject, message, from_email, [to_email])
        except Exception as e:
            return Response({'error': 'Failed to send reset email.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({'detail': 'Password reset email has been sent.'}, status=status.HTTP_200_OK)
    
@swagger_auto_schema(request_body=ResetPasswordRequestSerializer)
class PasswordResetConfirmView(APIView):
    permission_classes = [AllowAny]
    def post(self, request, *args, **kwargs):
        serializer = PasswordResetConfirmSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({'detail': 'Password has been reset successfully.'}, status=status.HTTP_200_OK)
    


class ProfileUpdateView(generics.RetrieveUpdateAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user.user_profile
    
    def put(self, request, *args, **kwargs):
        return Response({"detail": "Method PUT not allowed."}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
    

class ProfileListView(generics.ListAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

class ProfileRetrieveView(generics.RetrieveAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]
       