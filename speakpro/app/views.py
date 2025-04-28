# -*- coding: utf-8 -*-

# ==============================================================================
#                                COMMON IMPORTS
# ==============================================================================

# Django Imports
from django.shortcuts import render
from django.http import HttpResponse, FileResponse # FileResponse from view1
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, get_user_model
from django.core.cache import cache
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from datetime import timedelta
from django.core.files.storage import default_storage # from view1
from django.views.decorators.csrf import csrf_exempt # from view1

# DRF Imports
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.generics import ListCreateAPIView, ListAPIView, UpdateAPIView, DestroyAPIView, CreateAPIView
from rest_framework.filters import SearchFilter
from rest_framework.decorators import api_view # from view1

# Standard Library Imports
import random
import string
import os # from view1
import base64 # from view1
import tempfile # Để tạo file/thư mục tạm 
import difflib # Để mô phỏng so sánh text 
import re # Để tìm vị trí từ 
import shutil # Để dọn dẹp thư mục tạm 


# App Imports (Models & Serializers)
from .models import (
    Genre, SpeakingText, Audio, UserPracticeLog, Level, SpeakingResult, UserAudio # UserPracticeLog đã cập nhật
)
from .serializers import (
    GenreSerializer, SpeakingTextSerializer, AudioSerializer,
    ResetPasswordSerializer, UserPracticeLogSerializer, UserSerializer, # UserPracticeLogSerializer đã cập nhật
    LevelSerializer, UserAudioSerializer, SpeakingResultSerializer, # Bao gồm SpeakingResultSerializer từ file gốc
    # Serializers mới cho đánh giá phát âm 
    PronunciationAssessmentInputSerializer,
    PronunciationAssessmentResultSerializer,
    # PronunciationErrorSerializer (Được dùng bởi ResultSerializer)
)

# Third-party Imports for Pronunciation Assessment 
import speech_recognition as sr
from pydub import AudioSegment

# Import settings nếu cần lấy API keys (ví dụ cho Azure)
# from django.conf import settings


# ==============================================================================
#                             HELPER FUNCTIONS 
# ==============================================================================
# (Giữ các helper function từ lần merge trước và thêm helper mới)

# Helper function to split audio 
def split_audio_to_chunks(audio_path, chunk_length_ms=15000):
    """Splits a WAV audio file into chunks of specified length."""
    try:
        audio = AudioSegment.from_wav(audio_path)
        chunks = [audio[i:min(i + chunk_length_ms, len(audio))] for i in range(0, len(audio), chunk_length_ms)]
        return chunks
    except Exception as e:
        print(f"Error splitting audio {audio_path}: {e}")
        return []

# --- Helpers for Pronunciation Assessment  ---

# Placeholder cho hàm gọi Azure (bạn cần cài SDK và viết hàm này)
# def call_azure_pronunciation_assessment(audio_path, reference_text):
#     # ... (Code gọi Azure SDK như ở câu trả lời trước) ...
#     pass

# Hàm mô phỏng đánh giá và tìm lỗi (độ chính xác thấp)
def simulate_pronunciation_assessment(audio_path, reference_text):
    """
    Simulates assessment using basic STT and text comparison.
    NOTE: This is NOT accurate for phonetics or precise error location.
    Returns a dictionary matching the structure expected by PronunciationAssessmentResultSerializer.
    """
    print("--- Simulating Pronunciation Assessment ---")
    recognizer = sr.Recognizer()
    transcribed_text = ""
    wav_path = audio_path # Giả sử audio đã là WAV

    # 1. Speech-to-Text (using speech_recognition)
    try:
        with sr.AudioFile(wav_path) as source:
            audio_data = recognizer.record(source)
            transcribed_text = recognizer.recognize_google(audio_data, language="en-US")
            print(f"Simulated STT: '{transcribed_text}'")
    except sr.UnknownValueError:
        print("Simulation: Google Speech Recognition could not understand audio.")
        transcribed_text = "" # Return empty text if not recognized
    except sr.RequestError as e:
        print(f"Simulation: Could not request results from Google Speech Recognition service; {e}")
        raise sr.RequestError(f"Recognition service error: {e}")
    except Exception as e:
        print(f"Simulation: Error during STT: {e}")
        raise Exception(f"STT error: {e}")

    # 2. Text Comparison and Score Simulation (using difflib)
    ref_clean = re.sub(r'[^\w\s]', '', reference_text.lower())
    trans_clean = re.sub(r'[^\w\s]', '', transcribed_text.lower()) if transcribed_text else ""
    ref_words = ref_clean.split()
    trans_words = trans_clean.split()
    matcher = difflib.SequenceMatcher(None, ref_words, trans_words)
    similarity_ratio = matcher.ratio()
    pronunciation_score = max(0.0, min(100.0, round(similarity_ratio * 100, 2)))
    print(f"Simulated Score (text similarity): {pronunciation_score}")

    # 3. Error Identification Simulation
    errors_for_highlighting = []
    opcodes = matcher.get_opcodes()
    original_word_positions = []
    for match in re.finditer(r'\b\w+\b', reference_text):
        original_word_positions.append({
            "word": match.group(0), "start": match.start(), "end": match.end()
        })

    for tag, i1, i2, j1, j2 in opcodes:
        if tag != 'equal':
            try:
                if i1 < len(original_word_positions) and i2 <= len(original_word_positions) and i1 < i2:
                    start_word_index_orig = i1
                    end_word_index_orig = i2 - 1
                    error_word_span = " ".join(original_word_positions[k]['word'] for k in range(start_word_index_orig, end_word_index_orig + 1))
                    start_char_index = original_word_positions[start_word_index_orig]["start"]
                    end_char_index = original_word_positions[end_word_index_orig]["end"]
                    error_type = tag.capitalize()
                    errors_for_highlighting.append({
                        "word": error_word_span, "start_index": start_char_index,
                        "end_index": end_char_index, "error_type": error_type,
                        "suggestion": f"Check: '{error_word_span}'"
                    })
                else:
                    print(f"Warning: Could not accurately map error indices {i1}-{i2} to original text positions.")
            except IndexError:
                 print(f"Warning: Index error while mapping error indices {i1}-{i2}.")
            except Exception as map_e:
                 print(f"Warning: Error during error mapping: {map_e}")

    print(f"Simulated Errors Found: {len(errors_for_highlighting)}")

    return {
        "pronunciation_score": pronunciation_score,
        "transcribed_text": transcribed_text,
        "reference_text": reference_text,
        "errors": errors_for_highlighting, # Key là 'errors'
        "accuracy_score": None, "fluency_score": None, "completeness_score": None,
    }

# ==============================================================================
#                                  HOME VIEW
# ==============================================================================
def home(request):
    return HttpResponse("Speakpro")

# ==============================================================================
#                         AUTHENTICATION & USER MANAGEMENT VIEWS 
# ==============================================================================

class RegisterView(APIView):
    def post(self, request):
        data = request.data
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        confirm_password = data.get('confirm_password')

        if not all([username, email, password, confirm_password]):
             return Response({'error': 'Missing required fields!'}, status=status.HTTP_400_BAD_REQUEST)
        if password != confirm_password:
            return Response({'error': 'Passwords do not match!'}, status=status.HTTP_400_BAD_REQUEST)
        if User.objects.filter(username=username).exists():
             return Response({'error': 'Username already exists!'}, status=status.HTTP_400_BAD_REQUEST)
        if User.objects.filter(email=email).exists():
            return Response({'error': 'Email already exists!'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.create_user(username=username, email=email, password=password)
            return Response({'message': 'User registered successfully!'}, status=status.HTTP_201_CREATED)
        except Exception as e:
             print(f"Error during user registration: {e}")
             return Response({'error': 'Failed to register user.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class LoginView(APIView):
    def post(self, request):
        data = request.data
        username = data.get('username')
        password = data.get('password')

        if not username or not password:
            return Response({'error': 'Username and password are required!'}, status=status.HTTP_400_BAD_REQUEST)

        auth_user = authenticate(request, username=username, password=password)

        if auth_user is None:
            if User.objects.filter(username=username).exists():
                return Response({'message': 'Invalid password!'}, status=status.HTTP_401_UNAUTHORIZED)
            else:
                return Response({'message': 'User with this username does not exist!'}, status=status.HTTP_401_UNAUTHORIZED)
        try:
            refresh = RefreshToken.for_user(auth_user)
            # Sử dụng UserSerializer để trả về thông tin user an toàn
            user_data = UserSerializer(auth_user).data
            user_data.pop('password', None) # Xóa password khỏi response

            return Response({
                'refresh': str(refresh), # Trả về cả refresh token
                'access': str(refresh.access_token),
                'user': user_data
            }, status=status.HTTP_200_OK)
        except Exception as e:
             print(f"Error during token generation or user serialization: {e}")
             return Response({'error': 'Login failed during token generation.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class LogoutView(APIView):
    permission_classes = [IsAuthenticated] # Giữ nguyên permission

    def post(self, request):
        try:
            # Lấy refresh token từ request body (thường gửi key là 'refresh')
            refresh_token = request.data.get('refresh')
            if not refresh_token:
                 return Response({"error": "Refresh token ('refresh' key) is required in the request body."}, status=status.HTTP_400_BAD_REQUEST)
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"message": "Logged out successfully"}, status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            # Log lỗi và trả về lỗi chung chung
            print(f"Error during logout: {e}")
            # Có thể kiểm tra e là TokenError từ simplejwt để trả lỗi cụ thể hơn
            return Response({"error": "Logout failed. Invalid token or server error."}, status=status.HTTP_400_BAD_REQUEST)

class ForgotPasswordView(APIView):
    def post(self, request):
        email = request.data.get('email')
        if not email:
            return Response({'error': 'Email is required!'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            print(f"Password reset request for non-existent email: {email}")
            return Response({'message': 'If an account with this email exists, a confirmation code has been sent.'}, status=status.HTTP_200_OK)

        confirmation_code = ''.join(random.choices(string.ascii_letters + string.digits, k=6))
        cache_key = f"password_reset_code_{email}"
        cache.set(cache_key, confirmation_code, timeout=600) # 10 minutes

        try:
            send_mail(
                subject="Password Reset Confirmation Code - Speakpro",
                message=f"Hello {user.username or 'User'},\n\nYour confirmation code is: {confirmation_code}\nUse this code to reset your password. It will expire in 10 minutes.\n\nIf you did not request this, please ignore this email.",
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[email],
                fail_silently=False,
            )
            print(f"Password reset code sent to {email}")
            return Response({'message': 'Confirmation code sent to your email!'}, status=status.HTTP_200_OK)
        except Exception as e:
            print(f"Error sending password reset email to {email}: {e}")
            return Response({'error': 'Failed to send email. Please try again later or contact support.'},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class ResetPasswordView(APIView):
    def post(self, request):
        serializer = ResetPasswordSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        email = serializer.validated_data['email']
        confirmation_code = serializer.validated_data['confirmation_code']
        new_password = serializer.validated_data['new_password']

        cache_key = f"password_reset_code_{email}"
        cached_code = cache.get(cache_key)

        if not cached_code:
            return Response({'error': 'Expired confirmation code! Please request a new one.'}, status=status.HTTP_400_BAD_REQUEST)
        if cached_code != confirmation_code:
             return Response({'error': 'Invalid confirmation code!'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({'error': 'User with this email does not exist!'}, status=status.HTTP_404_NOT_FOUND)

        user.set_password(new_password)
        user.save()
        cache.delete(cache_key)
        print(f"Password reset successfully for {email}")

        return Response({'message': 'Password has been reset successfully!'}, status=status.HTTP_200_OK)

# ==============================================================================
#                         USER PROGRESS & HISTORY VIEWS 
# ==============================================================================
class UserPracticeLogView(ListCreateAPIView):
    """ API endpoint để xem/ghi lịch sử luyện tập. """
    serializer_class = UserPracticeLogSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return UserPracticeLog.objects.filter(user=user).select_related(
            'user', 'speaking_text', 'speaking_text__genre', 'speaking_text__level'
        ).order_by('-practice_date')

    def perform_create(self, serializer):
        # Gán user đang đăng nhập khi tạo log mới
        # Lưu ý: Endpoint này ít được dùng trực tiếp nếu assessment view tự lưu log
        serializer.save(user=self.request.user)

# ==============================================================================
#                            DASHBOARD & STATS VIEWS 
# ==============================================================================

User = get_user_model()
class DashboardStatsView(APIView):
    """ API endpoint lấy số liệu thống kê cho dashboard admin. """
    permission_classes = [IsAdminUser]

    def get(self, request, format=None):
        total_users = User.objects.count()
        active_users = User.objects.filter(is_active=True).count()
        recent_days = 7
        cutoff_date = timezone.now() - timedelta(days=recent_days)
        recent_activity_users = UserPracticeLog.objects.filter(
            practice_date__gte=cutoff_date
        ).values('user').distinct().count()

        data = {
            'total_users': total_users,
            'active_users': active_users,
            'recent_activity_users': recent_activity_users,
            'recent_activity_days': recent_days
        }
        return Response(data, status=status.HTTP_200_OK)


# ==============================================================================
#                         SPEAKPRO CORE API VIEWS 
# ==============================================================================
# API để lấy danh sách tất cả thể loại (APIView như gốc)
class GenreListView(APIView):
    def get(self, request):
        genres = Genre.objects.all().order_by('name')
        serializer = GenreSerializer(genres, many=True)
        return Response(serializer.data)

# API để lấy thể loại theo id 
class GenreDetailView(APIView):
    def get(self, request, pk):
        try:
            genre = Genre.objects.get(pk=pk)
            serializer = GenreSerializer(genre)
            return Response(serializer.data)
        except Genre.DoesNotExist:
            return Response({"error": "Genre not found"}, status=status.HTTP_404_NOT_FOUND)
        except ValueError: # Bắt lỗi nếu pk không phải số nguyên hợp lệ
             return Response({"error": "Invalid ID format."}, status=status.HTTP_400_BAD_REQUEST)


# API để lấy danh sách tất cả Speaking Texts 
class SpeakingTextListView(APIView):
    def get(self, request):
        texts = SpeakingText.objects.select_related('genre', 'level').all().order_by('title')
        serializer = SpeakingTextSerializer(texts, many=True, context={'request': request})
        return Response(serializer.data)

# API để lấy đoạn văn mẫu theo id 
class SpeakingTextDetailView(APIView):
    def get(self, request, pk):
        try:
            text = SpeakingText.objects.select_related('genre', 'level').get(pk=pk)
            serializer = SpeakingTextSerializer(text, context={'request': request})
            return Response(serializer.data)
        except SpeakingText.DoesNotExist:
            return Response({"error": "Speaking text not found"}, status=status.HTTP_404_NOT_FOUND)
        except ValueError:
             return Response({"error": "Invalid ID format."}, status=status.HTTP_400_BAD_REQUEST)


# API để lấy danh sách tất cả audio 
class AudioListView(APIView):
    def get(self, request):
        # Nên phân trang nếu danh sách quá lớn
        audios = Audio.objects.select_related('speaking_text').all()
        serializer = AudioSerializer(audios, many=True, context={'request': request})
        return Response(serializer.data)

# API để lấy audio theo id 
class AudioDetailView(APIView):
    def get(self, request, pk):
        try:
            audio = Audio.objects.get(pk=pk)
            if not audio.audio_file:
                return Response({"error": "Audio record exists but the file is missing."}, status=status.HTTP_404_NOT_FOUND)

            # Trả về URL tuyệt đối
            audio_url = request.build_absolute_uri(audio.audio_file.url)
            return Response({"audio_url": audio_url}, status=status.HTTP_200_OK)

        except Audio.DoesNotExist:
            return Response({"error": "Audio not found."}, status=status.HTTP_404_NOT_FOUND)
        except ValueError:
             return Response({"error": "Invalid ID format."}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
             print(f"Error generating audio URL for pk={pk}: {e}")
             return Response({"error": "Could not generate audio URL."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# API View để tìm kiếm SpeakingText (Topics) 
class SpeakingTextSearchView(ListAPIView):
    serializer_class = SpeakingTextSerializer
    permission_classes = [IsAuthenticated] # Yêu cầu đăng nhập để tìm kiếm
    filter_backends = [SearchFilter]
    search_fields = ['title', 'genre__name', 'level__name']
    queryset = SpeakingText.objects.select_related('genre', 'level').all().order_by('title')


# API để lọc SpeakingText theo genre và level (ListAPIView như gốc view1)
class SpeakingTextFilterAPIView(generics.ListAPIView):
    serializer_class = SpeakingTextSerializer
    permission_classes = [IsAuthenticated] # Yêu cầu đăng nhập

    def get_queryset(self):
        queryset = SpeakingText.objects.select_related('genre', 'level').all()
        genre_id = self.request.query_params.get('genre', None)
        level_id = self.request.query_params.get('level', None)
        if genre_id:
            try:
                queryset = queryset.filter(genre_id=int(genre_id))
            except (ValueError, TypeError):
                 pass # Bỏ qua nếu genre_id không hợp lệ
        if level_id:
            try:
                queryset = queryset.filter(level_id=int(level_id))
            except (ValueError, TypeError):
                 pass # Bỏ qua nếu level_id không hợp lệ
        return queryset.order_by('title')


# ==============================================================================
#                         AUDIO PROCESSING & SUBMISSION VIEWS 
# ==============================================================================

# Import utils nếu cần (đã import helper simulate_pronunciation_assessment)
# from .utils.audio_converter import convert_webm_to_mp3 # Giả sử có file này

@csrf_exempt # Cân nhắc dùng auth token thay csrf
@api_view(['POST'])
def upload_user_audio(request):
    # (Giữ nguyên logic gốc từ view1 hoặc phiên bản đã chỉnh sửa ở trên)
    audio_file = request.FILES.get('audio')
    user = request.user if request.user.is_authenticated else None

    # Xác định user 
    if not user:
        try:
            user = User.objects.get(username='tranv') # Hoặc trả lỗi yêu cầu đăng nhập
        except User.DoesNotExist:
            return Response({"error": "User context required. Please login or ensure test user exists."}, status=status.HTTP_401_UNAUTHORIZED)

    if not audio_file:
        return Response({"error": "No audio file provided ('audio' field)"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        # Lưu file gốc (ví dụ: webm) vào model UserAudio
        user_audio = UserAudio.objects.create(user=user, audio_file=audio_file)
        serializer = UserAudioSerializer(user_audio, context={'request': request})

        # --- Logic chuyển đổi (nếu cần thiết) ---
        # Ví dụ: chuyển webm -> mp3 như trong view1
        # input_path = user_audio.audio_file.path
        # filename_wo_ext = os.path.splitext(os.path.basename(input_path))[0]
        # converted_dir_name = 'converted_audio'
        # output_dir = os.path.join(settings.MEDIA_ROOT, converted_dir_name)
        # os.makedirs(output_dir, exist_ok=True)
        # output_path = os.path.join(output_dir, f"{filename_wo_ext}.mp3")
        #
        # success = convert_webm_to_mp3(input_path, output_path) # Gọi hàm chuyển đổi
        # if not success:
        #     user_audio.delete() # Xóa record nếu chuyển đổi lỗi
        #     return Response({"error": "Failed to convert audio."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        #
        # mp3_relative_path = os.path.join(converted_dir_name, f"{filename_wo_ext}.mp3")
        # mp3_absolute_url = request.build_absolute_uri(os.path.join(settings.MEDIA_URL, mp3_relative_path))
        #
        # return Response({
        #     'message': 'File uploaded and converted successfully.',
        #     'original_audio_url': serializer.data['audio_file'],
        #     'converted_audio_url': mp3_absolute_url
        # }, status=status.HTTP_201_CREATED)
        # --- Kết thúc logic chuyển đổi ---

        # Nếu không chuyển đổi, chỉ trả về thông tin file gốc
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    except Exception as e:
        print(f"Error during audio upload/conversion: {e}")
        if 'user_audio' in locals() and user_audio.pk:
             try: user_audio.delete() # Cleanup
             except: pass
        return Response({"error": "An unexpected error occurred during processing."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# API view cũ để submit và nhận diện 
class SubmitSpeakingAPIView(APIView):
    permission_classes = [IsAuthenticated] # Giữ permission

    def post(self, request):
        # (Giữ nguyên logic gốc từ view1 để nhận diện và tính điểm cơ bản)
        audio_file = request.FILES.get("audio_file")
        speaking_text_id = request.data.get("speaking_text_id")
        user = request.user

        if not audio_file or not speaking_text_id:
            return Response({"error": "Missing 'audio_file' or 'speaking_text_id'."}, status=status.HTTP_400_BAD_REQUEST)

        temp_dir = None
        wav_path = None
        recognized_text = ""

        try:
            # 1. Save and Convert Audio
            temp_dir = tempfile.mkdtemp(prefix="speakpro_submit_")
            temp_filename = f"{user.id}_{speaking_text_id}_{timezone.now().strftime('%Y%m%d%H%M%S%f')}.webm" # Thêm microsecond
            temp_path = os.path.join(temp_dir, temp_filename)

            with default_storage.open(temp_path, 'wb+') as destination:
                for chunk in audio_file.chunks():
                    destination.write(chunk)

            wav_path = temp_path.replace('.webm', '.wav')
            sound = AudioSegment.from_file(temp_path) # Tự nhận diện format
            sound = sound.set_channels(1)
            sound = sound.set_frame_rate(16000)
            sound.export(wav_path, format="wav")

            # 2. Speech Recognition (using chunks)
            recognizer = sr.Recognizer()
            chunks = split_audio_to_chunks(wav_path, chunk_length_ms=15000)
            if not chunks: raise Exception("Audio splitting failed.")

            for i, chunk in enumerate(chunks):
                chunk_path = f"{wav_path}_chunk_{i}.wav"
                chunk.export(chunk_path, format="wav")
                with sr.AudioFile(chunk_path) as source:
                    audio_data = recognizer.record(source)
                    try:
                        text = recognizer.recognize_google(audio_data, language="en-US")
                        recognized_text += text + " "
                    except sr.UnknownValueError:
                        print(f"[Warning] SubmitSpeaking Chunk {i}: could not understand audio.")
                    except sr.RequestError as e:
                        print(f"[Error] SubmitSpeaking Chunk {i}: recognition service error; {e}")
                if os.path.exists(chunk_path): os.remove(chunk_path) # Clean up chunk

            user_text_raw = recognized_text.strip()
            if not user_text_raw:
                 raise sr.UnknownValueError("No speech recognized from the audio.")

            # 3. Get Original Text & Calculate Score 
            speaking_text = SpeakingText.objects.get(id=speaking_text_id)

            # --- Logic lấy original_text từ SpeakingText.content ---
            original_text = ""
            if speaking_text.content:
                try:
                    content_hex = speaking_text.content.decode('utf-8')
                    content_binary = bytes.fromhex(content_hex)
                    original_text = content_binary.decode('utf-8')
                except Exception as decode_error:
                    print(f"Error decoding original text content ID {speaking_text_id}: {decode_error}")
                    raise Exception("Could not decode the original text content.")
            # --- Kết thúc logic lấy original_text ---


            # --- Logic tính điểm cũ (nếu có, ví dụ: calculate_score) ---
            # from .utils.score import calculate_score # Giả sử có hàm này
            # score_result = calculate_score(user_text_raw, original_text)
            # score_value = score_result.get("score", 0)
            # score_details = score_result.get("details") # Nếu có
            # --- Giả lập điểm nếu không có hàm calculate_score ---
            matcher = difflib.SequenceMatcher(None, original_text.lower(), user_text_raw.lower())
            score_value = round(matcher.ratio() * 100, 2)
            score_details = {"similarity_ratio": matcher.ratio()}
            # --- Kết thúc logic tính điểm cũ ---


            # 4. Save Result (ví dụ: vào SpeakingResult hoặc UserPracticeLog)
            # Ví dụ lưu vào SpeakingResult như view1
            SpeakingResult.objects.create(
                speaking_text=speaking_text,
                user_text=user_text_raw,
                score=score_value # Lưu điểm dạng Decimal nếu model yêu cầu
            )
            # Hoặc lưu vào UserPracticeLog
            # UserPracticeLog.objects.create(
            #      user=user,
            #      speaking_text=speaking_text,
            #      reference_text=original_text, # Lưu lại text gốc
            #      transcribed_text=user_text_raw,
            #      score=score_value,
            #      details=score_details # Lưu chi tiết điểm (nếu có)
            # )

            # 5. Return Result
            return Response({
                "recognized_text": user_text_raw,
                "original_text": original_text,
                "score": score_value,
                "details": score_details # Trả về details nếu có
            }, status=status.HTTP_200_OK)


        except SpeakingText.DoesNotExist:
            return Response({"error": "Reference speaking text not found."}, status=status.HTTP_404_NOT_FOUND)
        except sr.UnknownValueError:
            return Response({"error": "Could not understand audio or no speech detected."}, status=status.HTTP_400_BAD_REQUEST)
        except sr.RequestError as e:
            return Response({"error": f"Speech recognition service error: {e}"}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
        except Exception as e:
            print(f"Error in SubmitSpeakingAPIView: {e}")
            return Response({"error": "An unexpected error occurred during submission."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        finally:
            # Cleanup
            if temp_dir and os.path.exists(temp_dir):
                shutil.rmtree(temp_dir, ignore_errors=True)
            # Không xóa wav_path nếu nó nằm trong temp_dir đã bị xóa


# ==============================================================================
#                         CRUD OPERATIONS - SPEAKING TEXT 
# ==============================================================================

# API để thêm một SpeakingText mới 
class SpeakingTextCreateAPIView(APIView):
    permission_classes = [IsAdminUser] # Chỉ admin được tạo

    def post(self, request):
        # Dùng serializer để validate và tạo mới
        # Truyền context nếu serializer cần request
        serializer = SpeakingTextSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            try:
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except Exception as e:
                 print(f"Error saving SpeakingText: {e}")
                 return Response({"error": f"Failed to save SpeakingText: {e}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# API EDIT 
class SpeakingTextUpdateAPIView(generics.UpdateAPIView):
    queryset = SpeakingText.objects.all()
    serializer_class = SpeakingTextSerializer
    permission_classes = [IsAdminUser] # Chỉ admin được sửa
    lookup_field = 'id' # Tìm theo ID

# API DELETE 
class SpeakingTextDeleteAPIView(generics.DestroyAPIView):
    queryset = SpeakingText.objects.all()
    serializer_class = SpeakingTextSerializer # Dùng để xác nhận
    permission_classes = [IsAdminUser] # Chỉ admin được xóa
    lookup_field = 'id' # Tìm theo ID

# ==============================================================================
#                         CRUD OPERATIONS - USERS 
# ==============================================================================
# API để lấy danh sách người dùng 
class UserListView(APIView):
    permission_classes = [IsAdminUser] # Chỉ admin xem list user

    def get(self, request):
        users = User.objects.all().order_by('id')
        # Truyền context nếu serializer cần request
        serializer = UserSerializer(users, many=True, context={'request': request})
        return Response(serializer.data)


# API để tạo user
class UserCreateAPIView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer # Đảm bảo serializer hash password
    permission_classes = [IsAdminUser] # Chỉ admin tạo user qua API này

# API để cập nhật user 
class UserUpdateAPIView(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer # Đảm bảo xử lý password an toàn
    permission_classes = [IsAdminUser] # Hoặc logic cho phép user tự sửa profile
    lookup_field = 'id' # Tìm theo id

# API để xóa user 
class UserDeleteAPIView(generics.DestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser] # Chỉ admin xóa user
    lookup_field = 'id' # Tìm theo id

# ==============================================================================
#                                 LEVELS API
# ==============================================================================
# (Giữ nguyên class này từ view1.py)
class LevelListAPIView(generics.ListAPIView):
    queryset = Level.objects.all().order_by('id')
    serializer_class = LevelSerializer
    # Cho phép mọi user đã đăng nhập xem Levels
    permission_classes = [IsAuthenticated]


# ==============================================================================
#                         PRONUNCIATION ASSESSMENT API VIEW 
# ==============================================================================

class PronunciationAssessmentView(APIView):
    permission_classes = [IsAuthenticated] # Yêu cầu đăng nhập

    def post(self, request, *args, **kwargs):
        # --- 1. Validate Input ---
        input_serializer = PronunciationAssessmentInputSerializer(data=request.data)
        audio_file = request.FILES.get('audio_file')

        if not audio_file:
            return Response({"error": "Missing 'audio_file'."}, status=status.HTTP_400_BAD_REQUEST)
        if not input_serializer.is_valid():
            return Response(input_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        validated_data = input_serializer.validated_data
        reference_text = validated_data['reference_text']
        speaking_text_id = validated_data.get('speaking_text_id')
        user = request.user

        # --- 2. Process Audio File ---
        temp_dir = None
        wav_path = None
        try:
            temp_dir = tempfile.mkdtemp(prefix="speakpro_assess_")
            original_filename = audio_file.name
            safe_filename = re.sub(r'[^\w\.-]', '_', original_filename)
            original_extension = os.path.splitext(safe_filename)[1].lower()
            temp_original_path = os.path.join(temp_dir, f"input{original_extension}")

            with open(temp_original_path, 'wb+') as destination:
                for chunk in audio_file.chunks():
                    destination.write(chunk)

            wav_path = os.path.join(temp_dir, "processed_audio.wav")
            print(f"Processing audio: {temp_original_path} -> {wav_path}")
            sound = AudioSegment.from_file(temp_original_path)
            sound = sound.set_channels(1)
            sound = sound.set_frame_rate(16000)
            sound.export(wav_path, format="wav")
            print("Conversion to WAV successful.")

        except Exception as e:
            print(f"Error processing audio file: {e}")
            if temp_dir and os.path.exists(temp_dir):
                shutil.rmtree(temp_dir, ignore_errors=True)
            return Response({"error": f"Failed to process audio file. Ensure it is a valid audio format."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # --- 3. Perform Pronunciation Assessment ---
        assessment_result_data = None
        try:
            # CHỌN PHƯƠNG THỨC: Hiện tại dùng mô phỏng
            assessment_result_data = simulate_pronunciation_assessment(wav_path, reference_text)

            if not assessment_result_data:
                 raise Exception("Assessment function returned no result unexpectedly.")

        except sr.UnknownValueError as e:
             print(f"Assessment Error: Could not understand audio: {e}")
             return Response({"error": "Could not understand the speech in the audio file. Please try speaking more clearly.", "details": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except sr.RequestError as e:
             print(f"Assessment Error: Speech service unavailable: {e}")
             return Response({"error": "The speech recognition service is currently unavailable. Please try again later.", "details": str(e)}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
        except Exception as e:
            print(f"Unexpected error during pronunciation assessment: {e}")
            return Response({"error": "An unexpected error occurred during pronunciation assessment.", "details": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        finally:
            # --- 4. Cleanup Temporary Files ---
            if temp_dir and os.path.exists(temp_dir):
                try:
                    shutil.rmtree(temp_dir, ignore_errors=True)
                    print(f"Temporary directory {temp_dir} cleaned up.")
                except Exception as cleanup_error:
                    print(f"Warning: Error cleaning up temp directory {temp_dir}: {cleanup_error}")

        # --- 5. Save Practice Log ---
        try:
            speaking_text_instance = None
            if speaking_text_id:
                try:
                    speaking_text_instance = SpeakingText.objects.get(id=speaking_text_id)
                except SpeakingText.DoesNotExist:
                    print(f"Warning: SpeakingText with id={speaking_text_id} not found for logging.")

            log_details = {
                "pronunciation_score": assessment_result_data.get('pronunciation_score'),
                "accuracy_score": assessment_result_data.get('accuracy_score'),
                "fluency_score": assessment_result_data.get('fluency_score'),
                "completeness_score": assessment_result_data.get('completeness_score'),
                "errors_for_highlighting": assessment_result_data.get('errors', [])
            }

            log_entry = UserPracticeLog.objects.create(
                user=user,
                speaking_text=speaking_text_instance,
                reference_text=reference_text,
                transcribed_text=assessment_result_data.get('transcribed_text'),
                score=assessment_result_data.get('pronunciation_score'),
                details=log_details
            )
            print(f"Practice log saved with ID: {log_entry.id}")
        except Exception as log_error:
            print(f"CRITICAL: Error saving practice log: {log_error}")

        # --- 6. Prepare and Return Response using Serializer ---
        response_data = assessment_result_data
        output_serializer = PronunciationAssessmentResultSerializer(data=response_data)
        if output_serializer.is_valid():
             return Response(output_serializer.validated_data, status=status.HTTP_200_OK)
        else:
             print(f"CRITICAL: Output serializer errors: {output_serializer.errors}")
             print(f"Data passed to output serializer: {response_data}")
             return Response({"error": "Failed to serialize assessment results.", "serializer_errors": output_serializer.errors}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

