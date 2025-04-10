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

# ==============================================================================
#                         AUTHENTICATION & USER MANAGEMENT VIEWS
# ==============================================================================
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

# ==============================================================================
#                         USER PROGRESS & HISTORY VIEWS
# ==============================================================================
from rest_framework.generics import ListCreateAPIView # Dùng view này
from rest_framework.permissions import IsAuthenticated # Yêu cầu đăng nhập
from .models import UserPracticeLog, SpeakingText # Import model mới
from .serializers import UserPracticeLogSerializer # Import serializer mới
class UserPracticeLogView(ListCreateAPIView):
    """
    API endpoint để:
    - GET: Lấy lịch sử luyện tập của người dùng đang đăng nhập.
    - POST: Ghi lại một lượt luyện tập mới của người dùng đang đăng nhập.

    Khi POST, cần cung cấp:
    - speaking_text_id: ID của bài SpeakingText đã luyện tập.
    - score: Điểm số (nếu có).
    - details: Chi tiết JSON/text (nếu có).
    """
    serializer_class = UserPracticeLogSerializer
    permission_classes = [IsAuthenticated] # Bắt buộc đăng nhập để xem/ghi lịch sử

    def get_queryset(self):
        """
        Chỉ trả về lịch sử của người dùng đang đăng nhập.
        Sắp xếp theo ngày mới nhất.
        """
        user = self.request.user
        # select_related giúp tối ưu query, lấy thông tin user và speaking_text cùng lúc
        return UserPracticeLog.objects.filter(user=user).select_related('user', 'speaking_text', 'speaking_text__genre')

    def perform_create(self, serializer):
        """
        Tự động gán người dùng đang đăng nhập vào trường 'user' khi tạo log mới.
        """
        serializer.save(user=self.request.user)
            
# ==============================================================================
#                         SPEAKPRO CORE API VIEWS
# ==============================================================================

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Genre, SpeakingText, Audio
from .serializers import GenreSerializer, SpeakingTextSerializer, AudioSerializer
from django.http import HttpResponse
from rest_framework.generics import ListAPIView
from rest_framework.filters import SearchFilter



# API để lấy danh sách tất cả thể loại
class GenreListView(APIView):
    def get(self, request):
        genres = Genre.objects.all()
        serializer = GenreSerializer(genres, many=True)
        return Response(serializer.data)

# API để lấy thể loại theo id
class GenreDetailView(APIView):
    def get(self, request, pk):
        try:
            genre = Genre.objects.get(pk=pk)
        except Genre.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = GenreSerializer(genre)
        return Response(serializer.data)

class SpeakingTextListView(APIView):
    def get(self, request):
        texts = SpeakingText.objects.all()
        serializer = SpeakingTextSerializer(texts, many=True)
        return Response(serializer.data)

# API để lấy đoạn văn mẫu theo id
class SpeakingTextDetailView(APIView):
    def get(self, request, pk):
        try:
            text = SpeakingText.objects.get(pk=pk)
        except SpeakingText.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = SpeakingTextSerializer(text)
        return Response(serializer.data)

# API để lấy danh sách tất cả audio
class AudioListView(APIView):
    def get(self, request):
        audios = Audio.objects.all()
        serializer = AudioSerializer(audios, many=True)
        return Response(serializer.data)

# API để lấy audio theo id
class AudioDetailView(APIView):
    def get(self, request, pk):
        try:
            audio = Audio.objects.get(pk=pk)
        except Audio.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = AudioSerializer(audio)
        return Response(serializer.data)

# API View để tìm kiếm SpeakingText (Topics)
class SpeakingTextSearchView(ListAPIView):

    queryset = SpeakingText.objects.select_related('genre').all() # Tối ưu query bằng select_related
    serializer_class = SpeakingTextSerializer

    # Sử dụng bộ lọc SearchFilter của DRF
    filter_backends = [SearchFilter]
    # Chỉ định các trường sẽ được tìm kiếm
    # 'title': tìm trong trường title của SpeakingText
    # 'genre__name': tìm trong trường name của model Genre liên quan
    # (sử dụng __ để truy cập trường của related model)
    # Tiền tố '^', '=', '@', '$' có thể được dùng để thay đổi kiểu search (starts-with, exact, full-text, regex)
    # Mặc định là tìm kiếm chứa (case-insensitive contains)
    search_fields = ['title', 'genre__name']

