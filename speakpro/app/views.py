from django.shortcuts import render
from django.http import HttpResponse, FileResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework import generics
from rest_framework.filters import SearchFilter
import os
import base64
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from django.core.files.storage import default_storage


# Project-specific Models and Serializers (assuming they are in .models and .serializers)
from .models import Genre, SpeakingText, Audio, Level, SpeakingResult, UserAudio
from .serializers import GenreSerializer, SpeakingTextSerializer, AudioSerializer, UserSerializer, LevelSerializer, UserAudioSerializer, ResetPasswordSerializer

# Utils
from .utils.score import calculate_score
from .utils.audio_converter import convert_webm_to_mp3 # Assuming this is in .utils


def home(request):
    """Basic home view."""
    return HttpResponse("Speakpro API")

# ==============================================================================
#                         AUTHENTICATION & USER MANAGEMENT VIEWS
# ==============================================================================

# Imports specific to Authentication and User Management
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
import random
import string
from django.core.cache import cache
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth import get_user_model


class RegisterView(APIView):
    """API endpoint to register a new user."""
    def post(self, request):
        data = request.data

        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        confirm_password = data.get('confirm_password')

        # Check if passwords match
        if password != confirm_password:
            return Response({'error': 'Passwords do not match!'}, status=status.HTTP_400_BAD_REQUEST)

        # Check if email already exists
        if User.objects.filter(email=email).exists():
            return Response({'error': 'Email already exists!'}, status=status.HTTP_400_BAD_REQUEST)

        # Create the new user
        user = User.objects.create_user(
            username=username,  # Username is now the unique identifier
            email=email,  # Email used for login and notifications
            password=password
        )

        return Response({'message': 'User registered successfully!'}, status=status.HTTP_201_CREATED)


class LoginView(APIView):
    """API endpoint to log in a user and generate JWT tokens."""
    def post(self, request):
        data = request.data
        username = data.get('username')
        password = data.get('password')

        try:
            # Tìm kiếm người dùng dựa trên username
            user = User.objects.get(username=username)

            # Xác thực người dùng bằng username và mật khẩu
            auth_user = authenticate(request, username=user.username, password=password)

            if auth_user is None:
                return Response({'message': 'Invalid password!'},
                                status=status.HTTP_401_UNAUTHORIZED)

            # Tạo token
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
            return Response({'message': 'User with this username does not exist!'},
                            status=status.HTTP_401_UNAUTHORIZED)

class LogoutView(APIView):
    """API endpoint to log out a user by blacklisting the refresh token."""
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
    """API endpoint to send a password reset confirmation code to a user's email."""
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
    """API endpoint to reset a user's password using a confirmation code."""
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

# Imports specific to User Progress and History
from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import IsAuthenticated


class UserPracticeLogView(ListCreateAPIView):
    """
    API endpoint để:
    - GET: Lấy lịch sử luyện tập của người dùng đang đăng nhập.
    - POST: Ghi lại một lượt luyện tập mới của người dùng đang đăng nhập.

    Khi POST, cần cung cấp:
    - speaking_text_id: ID của bài SpeakingText đã luyện tập.
    - score: Điểm số.
    - details: Chi tiết JSON/text .
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
#                            DASHBOARD & STATS VIEWS
# ==============================================================================

# Imports specific to Dashboard and Stats
from django.utils import timezone
from datetime import timedelta
from rest_framework.permissions import IsAdminUser

User = get_user_model() # Ensure we are using the potentially swapped user model

class DashboardStatsView(APIView):
    """
    API endpoint lấy số liệu thống kê cho dashboard, sử dụng dữ liệu từ
    bảng `auth_user` và `app_userpracticelog`.
    """
    permission_classes = [IsAdminUser]

    def get(self, request, format=None):
        # 1. Tính Total Users: Đếm tất cả các dòng trong bảng `auth_user`
        total_users = User.objects.count()

        # 2. Tính Active Users: Đếm các dòng trong `auth_user` có trường `is_active` = True
        active_users = User.objects.filter(is_active=True).count()

        # 3. Tính Recent Activity Users:
        # Đếm số user_id *riêng biệt* trong `app_userpracticelog`
        # có `practice_date` trong vòng 7 ngày qua.
        recent_days = 7
        cutoff_date = timezone.now() - timedelta(days=recent_days)

        recent_activity_users = UserPracticeLog.objects.filter(
            practice_date__gte=cutoff_date
        ).values('user').distinct().count() # Dùng FK 'user' liên kết đến auth_user

        # Dữ liệu trả về cho Frontend
        data = {
            'total_users': total_users,
            'active_users': active_users,
            'recent_activity_users': recent_activity_users,
            'recent_activity_days': recent_days
        }

        return Response(data)

# ==============================================================================
#                         SPEAKPRO CORE API VIEWS
# ==============================================================================

# Imports specific to Speakpro Core API
import speech_recognition as sr
from pydub import AudioSegment


# API để lấy danh sách tất cả thể loại
class GenreListView(APIView):
    """API endpoint to get a list of all genres."""
    def get(self, request):
        genres = Genre.objects.all()
        serializer = GenreSerializer(genres, many=True)
        return Response(serializer.data)

# API để lấy thể loại theo id
class GenreDetailView(APIView):
    """API endpoint to get a specific genre by ID."""
    def get(self, request, pk):
        try:
            genre = Genre.objects.get(pk=pk)
        except Genre.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = GenreSerializer(genre)
        return Response(serializer.data)

#api lay sach theo level va genre
class SpeakingTextFilterAPIView(generics.ListAPIView):
    """API endpoint to filter SpeakingText by level and genre."""
    serializer_class = SpeakingTextSerializer

    def get_queryset(self):
        """
        Lọc danh sách tài liệu theo level và genre.
        """
        queryset = SpeakingText.objects.all()  # Lấy tất cả các tài liệu

        # Lọc theo genre nếu có
        genre_id = self.request.query_params.get('genre', None)
        if genre_id:
            queryset = queryset.filter(genre_id=genre_id)

        # Lọc theo level nếu có
        level_id = self.request.query_params.get('level', None)
        if level_id:
            queryset = queryset.filter(level_id=level_id)

        return queryset

class SpeakingTextListView(APIView):
    """API endpoint to get a list of all speaking texts."""
    def get(self, request):
        texts = SpeakingText.objects.all()
        serializer = SpeakingTextSerializer(texts, many=True)
        return Response(serializer.data)

# API để lấy đoạn văn mẫu theo id
class SpeakingTextDetailView(APIView):
    """API endpoint to get a specific speaking text by ID."""
    def get(self, request, pk):
        try:
            text = SpeakingText.objects.get(pk=pk)
        except SpeakingText.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = SpeakingTextSerializer(text)
        return Response(serializer.data)

# API để lấy danh sách tất cả audio
class AudioListView(APIView):
    """API endpoint to get a list of all audio files."""
    def get(self, request):
        audios = Audio.objects.all()
        serializer = AudioSerializer(audios, many=True)
        return Response(serializer.data)

# API để lấy audio theo id
class AudioDetailView(APIView):
    """API endpoint to get a specific audio file by ID and return its URL."""
    def get(self, request, pk):
        try:
            # Lấy đối tượng Audio từ cơ sở dữ liệu theo pk
            audio = Audio.objects.get(pk=pk)
        except Audio.DoesNotExist:
            return Response({"error": "Audio file not found."}, status=status.HTTP_404_NOT_FOUND)

        # Đảm bảo rằng tệp âm thanh tồn tại
        if not audio.audio_file:
            return Response({"error": "Audio file not found."}, status=status.HTTP_404_NOT_FOUND)

        # Trả về URL của tệp âm thanh (FileField sẽ tự động trả về URL)
        audio_url = audio.audio_file.url  # Lấy URL của tệp âm thanh
        # Construct full URL - adjust domain as needed for production
        full_audio_url = request.build_absolute_uri(audio_url)
        return Response({"audio_url": full_audio_url}, status=status.HTTP_200_OK)

# API View để tìm kiếm SpeakingText (Topics)
class SpeakingTextSearchView(ListAPIView):
    """API endpoint to search for SpeakingText (Topics) by title or genre name."""
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


@csrf_exempt
@api_view(['POST'])
def upload_user_audio(request):
    """API endpoint to upload user audio, convert it, and return URLs."""
    audio_file = request.FILES.get('audio')

    if audio_file:
        try:
            # Using request.user if authentication is in place,
            # otherwise, keep the test user for now.
            # Assuming authentication is handled before this view is called.
            user = request.user if request.user.is_authenticated else User.objects.get(username='tranv')
        except User.DoesNotExist:
            return Response({"error": "User does not exist."}, status=status.HTTP_400_BAD_REQUEST)

        # Lưu bản gốc .webm
        user_audio = UserAudio.objects.create(user=user, audio_file=audio_file)
        serializer = UserAudioSerializer(user_audio)

        # Đường dẫn file gốc
        input_path = user_audio.audio_file.path

        # Đường dẫn file .mp3 sau khi chuyển đổi
        filename_wo_ext = os.path.splitext(os.path.basename(input_path))[0]
        # Define a subdirectory within MEDIA_ROOT for converted audio
        output_subdir = 'converted_audio'
        output_filename = f"{filename_wo_ext}.mp3"
        output_path = os.path.join(settings.MEDIA_ROOT, output_subdir, output_filename)

        # Ensure the output directory exists
        os.makedirs(os.path.dirname(output_path), exist_ok=True)


        # Chuyển đổi WebM -> MP3
        success = convert_webm_to_mp3(input_path, output_path)
        if not success:
            # Clean up the original file if conversion fails
            user_audio.audio_file.delete()
            user_audio.delete()
            return Response({"error": "Failed to convert audio."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # Xây dựng URL tuyệt đối cho file .mp3
        mp3_relative_url = os.path.join(settings.MEDIA_URL, output_subdir, output_filename)
        mp3_absolute_url = request.build_absolute_uri(mp3_relative_url)

        # Optionally, save the path/URL of the converted audio in the UserAudio model
        # For now, we just return it in the response.

        return Response({
            'original_audio': serializer.data['audio_file'], # URL of original file
            'converted_audio': mp3_absolute_url
        }, status=status.HTTP_201_CREATED)

    return Response({"error": "No audio file provided"}, status=status.HTTP_400_BAD_REQUEST)

# Helper function (can be placed elsewhere, but keeping here for now)
def split_audio_to_chunks(audio_path, chunk_length_ms=15000):
    """Splits a WAV audio file into chunks."""
    # Imports specific to this function
    from pydub import AudioSegment
    audio = AudioSegment.from_wav(audio_path)
    chunks = [audio[i:i + chunk_length_ms] for i in range(0, len(audio), chunk_length_ms)]
    return chunks

class SubmitSpeakingAPIView(APIView):
    """API endpoint to submit user's speaking audio, process it, and calculate score."""
    def post(self, request):
        audio_file = request.FILES.get("audio_file")
        speaking_text_id = request.data.get("speaking_text_id")

        if not audio_file or not speaking_text_id:
            return Response({"error": "Thiếu dữ liệu"}, status=status.HTTP_400_BAD_REQUEST)

        # Lưu file tạm
        # Ensure a unique filename or handle potential naming conflicts
        temp_filename_webm = default_storage.get_available_name('temp_input.webm')
        temp_path_webm = default_storage.save(temp_filename_webm, audio_file)
        full_path_webm = os.path.join(default_storage.location, temp_path_webm)

        # Chuyển webm -> wav để nhận diện giọng nói
        wav_filename = os.path.splitext(temp_filename_webm)[0] + '.wav'
        wav_path = os.path.join(default_storage.location, default_storage.get_available_name(wav_filename))

        try:
            sound = AudioSegment.from_file(full_path_webm, format="webm")
            sound.export(wav_path, format="wav")
        except Exception as e:
            # Clean up temp files in case of conversion error
            default_storage.delete(temp_path_webm)
            return Response({"error": f"Không thể chuyển đổi file âm thanh: {e}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


        # Nhận diện văn bản từ wav
        recognizer = sr.Recognizer()
        user_text_raw = ""
        try:
            chunks = split_audio_to_chunks(wav_path, chunk_length_ms=15000)

            for i, chunk in enumerate(chunks):
                chunk_filename = f"chunk_part_{i}_{os.path.splitext(temp_filename_webm)[0]}.wav"
                chunk_path = os.path.join(default_storage.location, default_storage.get_available_name(chunk_filename))
                chunk.export(chunk_path, format="wav")

                with sr.AudioFile(chunk_path) as source:
                    try:
                         # Adjust recognizer settings if needed, e.g., phrase_time_limit
                        audio_data = recognizer.record(source)
                        text = recognizer.recognize_google(audio_data, language="en-US")
                        user_text_raw += " " + text
                    except sr.UnknownValueError:
                        print(f"[⚠️] Chunk {i}: không thể nhận diện.")
                        # Optionally, add a placeholder or handle silent parts
                        user_text_raw += " [unintelligible]"
                    except sr.RequestError as e:
                        print(f"[❌] Chunk {i}: lỗi kết nối Google API: {e}")
                        # Handle API errors, maybe add an error marker
                        user_text_raw += " [recognition error]"
                    finally:
                         # Clean up chunk file
                        default_storage.delete(chunk_path)

            user_text_raw = user_text_raw.strip()

        except Exception as e:
            # Clean up temp files if recognition fails
            default_storage.delete(temp_path_webm)
            default_storage.delete(wav_path)
            return Response({"error": f"Lỗi trong quá trình nhận diện giọng nói: {e}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


        # Lấy đoạn văn mẫu gốc
        try:
            speaking_text = SpeakingText.objects.get(id=speaking_text_id)
        except SpeakingText.DoesNotExist:
            # Clean up temp files
            default_storage.delete(temp_path_webm)
            default_storage.delete(wav_path)
            return Response({"error": "Văn bản mẫu không tồn tại"}, status=status.HTTP_404_NOT_FOUND)

        # Giải mã nội dung gốc
        original_text = ""
        if speaking_text.content:
            try:
                 # Assuming content is stored as binary data (bytes) from base64 decode
                original_text = speaking_text.content.decode("utf-8")
            except Exception as e:
                 # Clean up temp files
                default_storage.delete(temp_path_webm)
                default_storage.delete(wav_path)
                return Response({"error": f"Không thể giải mã nội dung đoạn văn mẫu: {e}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


        # Tính điểm và phân tích chi tiết từng từ
        # Ensure original_text is not empty before calculating score
        if not original_text:
             # Clean up temp files
            default_storage.delete(temp_path_webm)
            default_storage.delete(wav_path)
            return Response({"error": "Nội dung văn bản mẫu trống, không thể tính điểm."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        result = calculate_score(user_text_raw, original_text)

        # Lưu kết quả thô vào DB nếu muốn (tùy bạn)
        try:
            SpeakingResult.objects.create(
                speaking_text=speaking_text,
                user_text=user_text_raw,
                score=result.get("score", 0) # Use .get to avoid KeyError if score is missing
            )
        except Exception as e:
            print(f"Error saving SpeakingResult: {e}")
            # Continue even if saving result fails, but log the error

        # Dọn dẹp file tạm
        default_storage.delete(temp_path_webm)
        default_storage.delete(wav_path)


        # Trả kết quả
        return Response(result, status=status.HTTP_200_OK)


class UserListView(APIView):
    """API endpoint to get a list of all users (might require admin permission)."""
    # Consider adding permission_classes = [IsAdminUser] for security
    def get(self, request):
        users = User.objects.all()  # Lấy tất cả người dùng
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)


##################################################### CRUD TAI LIEU #######################################################

# API để thêm một SpeakingText mới
class SpeakingTextCreateAPIView(APIView):
    """API endpoint to create a new SpeakingText."""
    def post(self, request):
        genre_data = request.data.get('genre')  # Lấy dữ liệu genre từ request
        level_data = request.data.get('level')  # Lấy dữ liệu level từ request

        # Xử lý Genre
        genre = None
        if genre_data:
            if isinstance(genre_data, dict):  # Nếu genre được gửi dưới dạng dict (chứa name)
                genre_name = genre_data.get('name')
                if genre_name:
                    genre, created = Genre.objects.get_or_create(name=genre_name)
                else:
                     return Response({"error": "Genre name not provided in dictionary format."}, status=status.HTTP_400_BAD_REQUEST)
            else:  # Nếu genre là ID
                genre_id = genre_data
                try:
                    genre = Genre.objects.get(id=genre_id)
                except Genre.DoesNotExist:
                    return Response({"error": "Genre not found with the provided ID."}, status=status.HTTP_404_NOT_FOUND)
        else:
             return Response({"error": "Genre data not provided."}, status=status.HTTP_400_BAD_REQUEST)


        # Xử lý Level
        level = None
        if level_data:
            if isinstance(level_data, dict):  # Nếu level được gửi dưới dạng dict (chứa name)
                level_name = level_data.get('name')
                if level_name:
                     level, created = Level.objects.get_or_create(name=level_name)
                else:
                     return Response({"error": "Level name not provided in dictionary format."}, status=status.HTTP_400_BAD_REQUEST)
            else:  # Nếu level là ID
                level_id = level_data
                try:
                    level = Level.objects.get(id=level_id)
                except Level.DoesNotExist:
                    return Response({"error": "Level not found with the provided ID."}, status=status.HTTP_404_NOT_FOUND)
        else:
             return Response({"error": "Level data not provided."}, status=status.HTTP_400_BAD_REQUEST)


        # Giải mã nội dung content nếu có
        content_base64 = request.data.get('content')
        content_binary = None
        if content_base64:
            try:
                content_binary = base64.b64decode(content_base64)  # Giải mã base64 thành binary
            except Exception as e:
                 return Response({"error": f"Không thể giải mã nội dung content base64: {e}"}, status=status.HTTP_400_BAD_REQUEST)


        # Tạo SpeakingText và lưu vào cơ sở dữ liệu
        # Prepare data for serializer, excluding genre and level which are handled separately
        serializer_data = request.data.copy()
        serializer_data.pop('genre', None) # Remove to avoid serializer trying to handle it
        serializer_data.pop('level', None) # Remove to avoid serializer trying to handle it
        serializer_data['content'] = content_binary # Add the processed content

        serializer = SpeakingTextSerializer(data=serializer_data)

        if serializer.is_valid():
            # Liên kết với genre và level, lưu content đã giải mã vào cơ sở dữ liệu
            serializer.save(genre=genre, level=level)  # Lưu vào cơ sở dữ liệu
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#API EDIT
class SpeakingTextUpdateAPIView(generics.UpdateAPIView):
    """API endpoint to update an existing SpeakingText by ID."""
    queryset = SpeakingText.objects.all()  # Lấy tất cả tài liệu
    serializer_class = SpeakingTextSerializer  # Sử dụng SpeakingTextSerializer để cập nhật
    lookup_field = 'id'  # Để tìm tài liệu theo ID

#API DELETE
class SpeakingTextDeleteAPIView(generics.DestroyAPIView):
    """API endpoint to delete a SpeakingText by ID."""
    queryset = SpeakingText.objects.all()  # Lấy tất cả tài liệu
    serializer_class = SpeakingTextSerializer  # Dùng serializer của SpeakingText
    lookup_field = 'id'  # Tìm tài liệu theo ID


##################################################### CRUD USER #######################################################
class UserCreateAPIView(generics.CreateAPIView):
    """API endpoint to create a new user."""
    queryset = User.objects.all()  # Tất cả người dùng
    serializer_class = UserSerializer  # Dùng UserSerializer để tạo mới người dùng

class UserUpdateAPIView(generics.UpdateAPIView):
    """API endpoint to update an existing user by ID."""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'id'  # Tìm người dùng theo id

class UserDeleteAPIView(generics.DestroyAPIView):
    """API endpoint to delete a user by ID."""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'id'  # Tìm người dùng theo id

class LevelListAPIView(generics.ListAPIView):
    """API endpoint to get a list of all levels."""
    queryset = Level.objects.all()  # Lấy tất cả các level
    serializer_class = LevelSerializer  # Sử dụng LevelSerializer để trả về dữ liệu