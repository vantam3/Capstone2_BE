from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
import random
import string
from django.core.cache import cache
from django.core.mail import send_mail
from django.conf import settings
from .serializers import ResetPasswordSerializer 

def home(request):
    return HttpResponse("Speakpro")

class RegisterView(APIView):
    def post(self, request):
        data = request.data
        username = data.get('email')
        password = data.get('password')
        confirm_password = data.get('confirm_password')
        first_name = data.get('first_name', '')
        last_name = data.get('last_name', '')

        if password != confirm_password:
            return Response({'error': 'Passwords do not match!'}, status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(username=username).exists():
            return Response({'error': 'Email already exists!'}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.create_user(
            username=username,
            email=username,
            password=password,
            first_name=first_name,
            last_name=last_name
        )
        return Response({'message': 'User registered successfully!'}, status=status.HTTP_201_CREATED)
    
class LoginView(APIView):
    def post(self, request):
        data = request.data
        email = data.get('email')
        password = data.get('password')

        try:
            # Lookup user by email
            user = User.objects.get(email=email)

            # Authenticate using the user's username
            auth_user = authenticate(request, username=user.username, password=password)

            if auth_user is None:
                return Response({'message': 'Invalid password!'}, 
                                status=status.HTTP_401_UNAUTHORIZED)

            # Generate token
            refresh = RefreshToken.for_user(auth_user)
            return Response({
                'token': str(refresh.access_token),
                'user': {
                    'id': auth_user.id,
                    'first_name': auth_user.first_name,
                    'last_name': auth_user.last_name,
                    'email': auth_user.email,
                    'is_superuser': auth_user.is_superuser,
                }
            }, status=status.HTTP_200_OK)

        except User.DoesNotExist:
            return Response({'message': 'User with this email does not exist!'}, 
                            status=status.HTTP_401_UNAUTHORIZED)

class LogoutView(APIView):
    def post(self, request):
        try:
            # Lấy refresh token từ request
            refresh_token = request.data.get('refresh_token')
            token = RefreshToken(refresh_token)
            token.blacklist()  # Thêm token vào danh sách blacklist

            return Response({"message": "Logged out successfully"}, status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class ForgotPasswordView(APIView):
    def post(self, request):
        email = request.data.get('email')
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({'error': 'User with this email does not exist!'}, status=status.HTTP_404_NOT_FOUND)

        # Generate a confirmation code
        confirmation_code = ''.join(random.choices(string.ascii_letters + string.digits, k=6))

        # Store the confirmation code in cache with a timeout (e.g., 10 minutes)
        cache.set(f"password_reset_code_{email}", confirmation_code, timeout=600)

        try:
            send_mail(
                subject="Confirmation Code - Bookquest",
                message=f"Hello {user.first_name},\n\nYour confirmation code is: {confirmation_code}\nUse this code to reset your password.",
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[email],
                fail_silently=False,
            )
            return Response({'message': 'Confirmation code sent to your email!'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': 'Failed to send email. Please try again later.', 'details': str(e)}, 
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
class ResetPasswordView(APIView):
    def post(self, request):
        serializer = ResetPasswordSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        email = serializer.validated_data['email']
        confirmation_code = serializer.validated_data['confirmation_code']
        new_password = serializer.validated_data['new_password']

        # Retrieve the confirmation code from cache
        cached_code = cache.get(f"password_reset_code_{email}")

        if not cached_code or cached_code != confirmation_code:
            return Response({'error': 'Invalid or expired confirmation code!'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({'error': 'User with this email does not exist!'}, status=status.HTTP_404_NOT_FOUND)

        # Update the password
        user.set_password(new_password)
        user.save()

        # Clear the confirmation code from cache
        cache.delete(f"password_reset_code_{email}")

        return Response({'message': 'Password has been reset successfully!'}, status=status.HTTP_200_OK)
            
