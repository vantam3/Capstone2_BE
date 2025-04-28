# -*- coding: utf-8 -*-

# ==============================================================================
#                                COMMON IMPORTS
# ==============================================================================

# Django Imports
from django.shortcuts import render
from django.http import HttpResponse, FileResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, get_user_model
from django.core.cache import cache
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from datetime import timedelta
from django.core.files.storage import default_storage
from django.views.decorators.csrf import csrf_exempt

# DRF Imports
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.generics import ListCreateAPIView, ListAPIView, UpdateAPIView, DestroyAPIView, CreateAPIView
from rest_framework.filters import SearchFilter
from rest_framework.decorators import api_view

# Standard Library Imports
import random
import string
import os
import base64
import tempfile # Để tạo file/thư mục tạm (MỚI)
import difflib # Để mô phỏng so sánh text (MỚI)
import re # Để tìm vị trí từ (MỚI)
import shutil # Để dọn dẹp thư mục tạm (MỚI)

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
    PronunciationErrorSerializer # Mặc dù không dùng trực tiếp trong view, import để rõ ràng
)

# Third-party Imports for Pronunciation Assessment
import speech_recognition as sr # (MỚI)
from pydub import AudioSegment # (MỚI)

# Import settings nếu cần lấy API keys (ví dụ cho Azure)
# from django.conf import settings


# ==============================================================================
#                             HELPER FUNCTIONS
# ==============================================================================

# Placeholder cho hàm gọi Azure (cần cài SDK và viết hàm này)
# def call_azure_pronunciation_assessment(audio_path, reference_text):
#     # Cài đặt: pip install azure-cognitiveservices-speech
#     import azure.cognitiveservices.speech as speechsdk
#     print("--- Calling Azure Pronunciation Assessment ---")
#     # Lấy key và region từ settings hoặc environment variables
#     speech_key = getattr(settings, "AZURE_SPEECH_KEY", None)
#     service_region = getattr(settings, "AZURE_SPEECH_REGION", None)
#
#     if not speech_key or not service_region:
#         print("Azure credentials not configured.")
#         raise ValueError("Azure credentials (AZURE_SPEECH_KEY, AZURE_SPEECH_REGION) not configured in settings.")
#
#     speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)
#     audio_config = speechsdk.audio.AudioConfig(filename=audio_path)
#
#     # Tạo pronunciation assessment config
#     pronunciation_config = speechsdk.PronunciationAssessmentConfig(
#         reference_text=reference_text,
#         grading_system=speechsdk.PronunciationAssessmentGradingSystem.HundredMark,
#         granularity=speechsdk.PronunciationAssessmentGranularity.Phoneme, # Hoặc Word, Phoneme cho chi tiết nhất
#         enable_miscue="True" # Phát hiện từ thừa/thiếu
#     )
#
#     # Tạo speech recognizer với assessment config
#     # Chỉ định ngôn ngữ phù hợp, ví dụ 'en-US'
#     recognizer = speechsdk.SpeechRecognizer(
#         speech_config=speech_config,
#         audio_config=audio_config,
#         language="en-US"
#     )
#     pronunciation_config.apply_to(recognizer)
#
#     # Bắt đầu nhận diện và lấy kết quả
#     result = recognizer.recognize_once()
#     assessment_result = {}
#
#     if result.reason == speechsdk.ResultReason.RecognizedSpeech:
#         pronunciation_result = speechsdk.PronunciationAssessmentResult(result)
#         assessment_result = {
#             "pronunciation_score": pronunciation_result.pronunciation_score,
#             "accuracy_score": pronunciation_result.accuracy_score,
#             "fluency_score": pronunciation_result.fluency_score,
#             "completeness_score": pronunciation_result.completeness_score,
#             "transcribed_text": result.text,
#             "words": [
#                 {
#                     "word": word.word,
#                     "accuracy_score": word.accuracy_score,
#                     "error_type": word.error_type,
#                     "offset": word.offset / 10000, # convert ticks to ms
#                     "duration": word.duration / 10000 # convert ticks to ms
#                 } for word in pronunciation_result.words
#             ]
#         }
#         print(f"Azure Assessment successful: Score={assessment_result['pronunciation_score']}")
#         return assessment_result
#     elif result.reason == speechsdk.ResultReason.NoMatch:
#         print("Azure Assessment: No speech could be recognized.")
#         raise sr.UnknownValueError("Azure: No speech could be recognized.")
#     elif result.reason == speechsdk.ResultReason.Canceled:
#         cancellation_details = result.cancellation_details
#         print(f"Azure Assessment: Speech Recognition canceled: {cancellation_details.reason}")
#         if cancellation_details.reason == speechsdk.CancellationReason.Error:
#             print(f"Azure Assessment: Error details: {cancellation_details.error_details}")
#         raise Exception(f"Azure recognition canceled: {cancellation_details.reason}")
#
#     return None # Should not reach here ideally

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
            # Consider adding noise reduction if needed: recognizer.adjust_for_ambient_noise(source)
            audio_data = recognizer.record(source)
            transcribed_text = recognizer.recognize_google(audio_data, language="en-US")
            print(f"Simulated STT: '{transcribed_text}'")
    except sr.UnknownValueError:
        print("Simulation: Google Speech Recognition could not understand audio.")
        transcribed_text = "" # Return empty text if not recognized
    except sr.RequestError as e:
        print(f"Simulation: Could not request results from Google Speech Recognition service; {e}")
        # Decide how to handle this: re-raise, return specific error, or continue with empty text
        raise sr.RequestError(f"Recognition service error: {e}")
    except Exception as e:
        print(f"Simulation: Error during STT: {e}")
        raise Exception(f"STT error: {e}")

    # 2. Text Comparison and Score Simulation (using difflib)
    # Normalize text for better comparison (lowercase, remove punctuation)
    ref_clean = re.sub(r'[^\w\s]', '', reference_text.lower())
    trans_clean = re.sub(r'[^\w\s]', '', transcribed_text.lower()) if transcribed_text else ""

    ref_words = ref_clean.split()
    trans_words = trans_clean.split()

    matcher = difflib.SequenceMatcher(None, ref_words, trans_words)
    similarity_ratio = matcher.ratio()
    # Ensure score is between 0 and 100
    pronunciation_score = max(0.0, min(100.0, round(similarity_ratio * 100, 2)))
    print(f"Simulated Score (text similarity): {pronunciation_score}")

    # 3. Error Identification Simulation (Finding differing words and estimating position)
    errors_for_highlighting = []
    opcodes = matcher.get_opcodes() # ('equal', i1, i2, j1, j2), ('replace', i1, i2, j1, j2), etc.

    # Find word start/end indices in the ORIGINAL reference_text
    original_word_positions = []
    # Use finditer to get match objects with start/end indices
    for match in re.finditer(r'\b\w+\b', reference_text): # Use original text here!
        original_word_positions.append({
            "word": match.group(0),
            "start": match.start(),
            "end": match.end()
        })

    # Map opcodes (which use cleaned word indices) back to original word indices and positions
    current_original_word_index = 0
    ref_word_map = {i: original_word_positions[i] for i in range(len(original_word_positions))}
    # Need to align cleaned words (used in difflib) back to original words if punctuation was removed

    # This mapping is tricky if punctuation removal changes word count/indices significantly.
    # A simpler approach for simulation might be to find the *span* of the differing words in the original text.

    for tag, i1, i2, j1, j2 in opcodes:
        if tag != 'equal':
            # Indices i1, i2 refer to the *cleaned* ref_words list
            # We need to find the corresponding words and their positions in the *original* text
            try:
                # Find the start index in original text corresponding to ref_words[i1]
                # Find the end index in original text corresponding to ref_words[i2-1]
                # This requires a robust mapping, which is complex.
                # Simplified approach: Use the indices i1, i2 directly on original_word_positions
                # This assumes word count is the same, which might be wrong due to punctuation.

                if i1 < len(original_word_positions) and i2 <= len(original_word_positions) and i1 < i2 :
                    start_word_index_orig = i1
                    end_word_index_orig = i2 - 1

                    error_word_span = " ".join(original_word_positions[k]['word'] for k in range(start_word_index_orig, end_word_index_orig + 1))
                    start_char_index = original_word_positions[start_word_index_orig]["start"]
                    end_char_index = original_word_positions[end_word_index_orig]["end"]
                    error_type = tag.capitalize() # Replace, Delete, Insert

                    errors_for_highlighting.append({
                        "word": error_word_span,
                        "start_index": start_char_index,
                        "end_index": end_char_index,
                        "error_type": error_type,
                        "suggestion": f"Check: '{error_word_span}'" # Generic suggestion
                    })
                else:
                    # Fallback or log if indices are out of bounds
                     print(f"Warning: Could not accurately map error indices {i1}-{i2} to original text positions.")

            except IndexError:
                 print(f"Warning: Index error while mapping error indices {i1}-{i2}.")
            except Exception as map_e:
                 print(f"Warning: Error during error mapping: {map_e}")


    print(f"Simulated Errors Found: {len(errors_for_highlighting)}")

    return {
        "pronunciation_score": pronunciation_score,
        "transcribed_text": transcribed_text,
        "reference_text": reference_text, # Return original text
        "errors": errors_for_highlighting, # Use the key 'errors' as defined in the result serializer
        # Other scores are null in simulation
        "accuracy_score": None,
        "fluency_score": None,
        "completeness_score": None,
    }


# Helper function to split audio (from previous merge)
def split_audio_to_chunks(audio_path, chunk_length_ms=15000):
    """Splits a WAV audio file into chunks of specified length."""
    try:
        audio = AudioSegment.from_wav(audio_path)
        chunks = [audio[i:min(i + chunk_length_ms, len(audio))] for i in range(0, len(audio), chunk_length_ms)]
        return chunks
    except Exception as e:
        print(f"Error splitting audio {audio_path}: {e}")
        return [] # Return empty list on error


# ==============================================================================
#                                  HOME VIEW
# ==============================================================================
def home(request):
    return HttpResponse("Speakpro API") # Updated name slightly

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

        # Authenticate using username and password
        auth_user = authenticate(request, username=username, password=password)

        if auth_user is None:
            # Check if the user exists but password was wrong
            if User.objects.filter(username=username).exists():
                return Response({'message': 'Invalid password!'}, status=status.HTTP_401_UNAUTHORIZED)
            else:
                return Response({'message': 'User with this username does not exist!'}, status=status.HTTP_401_UNAUTHORIZED)

        # Generate tokens
        try:
            refresh = RefreshToken.for_user(auth_user)
            # Serialize user data carefully, avoid sending sensitive info
            user_data = UserSerializer(auth_user).data
            # Remove password field from response even if it's write_only in serializer
            user_data.pop('password', None)

            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user': user_data
            }, status=status.HTTP_200_OK)
        except Exception as e:
            print(f"Error during token generation or user serialization: {e}")
            return Response({'error': 'Login failed during token generation.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class LogoutView(APIView):
    permission_classes = [IsAuthenticated] # Must be logged in to log out

    def post(self, request):
        try:
            refresh_token = request.data.get('refresh') # Standard key for refresh token
            if not refresh_token:
                 return Response({"error": "Refresh token is required"}, status=status.HTTP_400_BAD_REQUEST)
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"message": "Logged out successfully"}, status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            # Catch specific token errors if possible (e.g., TokenError from simplejwt)
            print(f"Error during logout: {e}")
            return Response({"error": "Logout failed. Invalid token or server error."}, status=status.HTTP_400_BAD_REQUEST)

class ForgotPasswordView(APIView):
    def post(self, request):
        email = request.data.get('email')
        if not email:
            return Response({'error': 'Email is required!'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            # Avoid revealing if email exists - return success-like message regardless
            print(f"Password reset request for non-existent email: {email}")
            return Response({'message': 'If an account with this email exists, a confirmation code has been sent.'}, status=status.HTTP_200_OK)

        confirmation_code = ''.join(random.choices(string.ascii_letters + string.digits, k=6))
        cache_key = f"password_reset_code_{email}"
        cache.set(cache_key, confirmation_code, timeout=600) # 10 minutes timeout

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
            # Don't expose detailed error to client
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
            # Should not happen if ForgotPasswordView doesn't reveal existence, but handle defensively
            return Response({'error': 'User with this email does not exist!'}, status=status.HTTP_404_NOT_FOUND)

        # Update the password and save
        user.set_password(new_password)
        user.save()

        # Clear the confirmation code from cache
        cache.delete(cache_key)
        print(f"Password reset successfully for {email}")

        return Response({'message': 'Password has been reset successfully!'}, status=status.HTTP_200_OK)

# ==============================================================================
#                         USER PROGRESS & HISTORY VIEWS
# ==============================================================================
class UserPracticeLogView(ListCreateAPIView):
    """
    API endpoint for user practice history.
    - GET: Fetch practice history for the logged-in user.
    - POST: Record a new practice session (typically done by the assessment endpoint now).
            Keeping POST might be useful for manually adding logs if needed.
    """
    serializer_class = UserPracticeLogSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Return history for the current user, newest first."""
        user = self.request.user
        return UserPracticeLog.objects.filter(user=user).select_related(
            'user', 'speaking_text', 'speaking_text__genre', 'speaking_text__level'
        ).order_by('-practice_date')

    def perform_create(self, serializer):
        """Assign the logged-in user automatically."""
        serializer.save(user=self.request.user)

# ==============================================================================
#                            DASHBOARD & STATS VIEWS
# ==============================================================================
User = get_user_model() # Ensure User is the correct model

class DashboardStatsView(APIView):
    """Admin dashboard statistics."""
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
#                         SPEAKPRO CORE API VIEWS (Content Management)
# ==============================================================================

# --- Genre Views ---
class GenreListView(generics.ListCreateAPIView): # Use generics for standard list/create
    queryset = Genre.objects.all().order_by('name')
    serializer_class = GenreSerializer
    # Allow authenticated users to view, admins to create
    permission_classes = [IsAuthenticated]
    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAdminUser()]
        return super().get_permissions()

class GenreDetailView(generics.RetrieveUpdateDestroyAPIView): # Use generics for standard RUD
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [IsAdminUser] # Only admins can modify/delete genres
    lookup_field = 'pk'

# --- Level Views ---
class LevelListView(generics.ListCreateAPIView): # Use generics
    queryset = Level.objects.all().order_by('id') # Order by ID or name
    serializer_class = LevelSerializer
    permission_classes = [IsAuthenticated] # Similar permissions as Genre
    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAdminUser()]
        return super().get_permissions()

class LevelDetailView(generics.RetrieveUpdateDestroyAPIView): # Use generics
    queryset = Level.objects.all()
    serializer_class = LevelSerializer
    permission_classes = [IsAdminUser]
    lookup_field = 'pk'


# --- SpeakingText (Topics) Views ---
class SpeakingTextListView(generics.ListAPIView): # List only, creation separate
    queryset = SpeakingText.objects.select_related('genre', 'level').all().order_by('title')
    serializer_class = SpeakingTextSerializer
    permission_classes = [IsAuthenticated] # Allow viewing by logged-in users

# Separate Create view for SpeakingText
class SpeakingTextCreateView(generics.CreateAPIView):
     queryset = SpeakingText.objects.all()
     serializer_class = SpeakingTextSerializer
     permission_classes = [IsAdminUser] # Only admins create texts

class SpeakingTextDetailView(generics.RetrieveAPIView): # Retrieve only
    queryset = SpeakingText.objects.select_related('genre', 'level').all()
    serializer_class = SpeakingTextSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'pk'

class SpeakingTextUpdateView(generics.UpdateAPIView): # Update only
     queryset = SpeakingText.objects.all()
     serializer_class = SpeakingTextSerializer
     permission_classes = [IsAdminUser]
     lookup_field = 'pk' # Use pk or id

class SpeakingTextDeleteView(generics.DestroyAPIView): # Delete only
     queryset = SpeakingText.objects.all()
     serializer_class = SpeakingTextSerializer
     permission_classes = [IsAdminUser]
     lookup_field = 'pk' # Use pk or id


# API to filter Speaking Texts by genre and/or level
class SpeakingTextFilterAPIView(generics.ListAPIView):
    serializer_class = SpeakingTextSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = SpeakingText.objects.select_related('genre', 'level').all()
        genre_id = self.request.query_params.get('genre', None)
        level_id = self.request.query_params.get('level', None)
        if genre_id:
            queryset = queryset.filter(genre_id=genre_id)
        if level_id:
            queryset = queryset.filter(level_id=level_id)
        return queryset.order_by('title')

# API View for searching Speaking Texts (Topics)
class SpeakingTextSearchView(ListAPIView):
    serializer_class = SpeakingTextSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [SearchFilter]
    search_fields = ['title', 'genre__name', 'level__name'] # Search title, genre name, level name
    queryset = SpeakingText.objects.select_related('genre', 'level').all().order_by('title')


# --- Audio Views (Reference Audio for Speaking Texts) ---
class AudioListView(generics.ListCreateAPIView): # Use generics
    queryset = Audio.objects.select_related('speaking_text').all()
    serializer_class = AudioSerializer
    permission_classes = [IsAdminUser] # Only admins manage reference audio

class AudioDetailView(generics.RetrieveUpdateDestroyAPIView): # Use generics
    queryset = Audio.objects.all()
    serializer_class = AudioSerializer
    permission_classes = [IsAdminUser]
    lookup_field = 'pk'

# ==============================================================================
#                         AUDIO PROCESSING & SUBMISSION VIEWS
# ==============================================================================

# Note: The old `upload_user_audio` and `SubmitSpeakingAPIView` are now superseded
# by the `PronunciationAssessmentView`. You might remove them or keep them for other purposes.

# If keeping upload_user_audio for general uploads:
@csrf_exempt
@api_view(['POST'])
def upload_user_audio(request):
     # (Code from previous merge, ensure it uses UserAudio model and UserAudioSerializer)
     # Consider adding authentication here using @permission_classes([IsAuthenticated])
     audio_file = request.FILES.get('audio')
     user = request.user if request.user.is_authenticated else None
     if not user:
         # Handle anonymous upload or require login
         return Response({"error": "Authentication required."}, status=status.HTTP_401_UNAUTHORIZED)
     if not audio_file:
         return Response({"error": "No audio file provided ('audio' field)"}, status=status.HTTP_400_BAD_REQUEST)
     try:
         # Save using UserAudio model
         user_audio = UserAudio.objects.create(user=user, audio_file=audio_file)
         serializer = UserAudioSerializer(user_audio, context={'request': request})
         return Response(serializer.data, status=status.HTTP_201_CREATED)
     except Exception as e:
         print(f"Error uploading user audio: {e}")
         return Response({"error": "Failed to upload audio."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# ==============================================================================
#                         PRONUNCIATION ASSESSMENT API VIEW (MỚI)
# ==============================================================================

class PronunciationAssessmentView(APIView):
    permission_classes = [IsAuthenticated] # Yêu cầu đăng nhập

    def post(self, request, *args, **kwargs):
        # --- 1. Validate Input ---
        input_serializer = PronunciationAssessmentInputSerializer(data=request.data)
        audio_file = request.FILES.get('audio_file') # Tên field chuẩn cho file

        if not audio_file:
            return Response({"error": "Missing 'audio_file'."}, status=status.HTTP_400_BAD_REQUEST)

        # Validate file size, type if needed
        # MAX_UPLOAD_SIZE = 5 * 1024 * 1024 # Example: 5MB
        # if audio_file.size > MAX_UPLOAD_SIZE:
        #    return Response({"error": f"Audio file size exceeds limit ({MAX_UPLOAD_SIZE // 1024 // 1024}MB)."}, status=status.HTTP_400_BAD_REQUEST)
        # allowed_types = ['audio/mpeg', 'audio/wav', 'audio/webm', 'audio/ogg', 'audio/mp4'] # Adjust as needed
        # if audio_file.content_type not in allowed_types:
        #    return Response({"error": f"Unsupported audio file type: {audio_file.content_type}. Allowed: {', '.join(allowed_types)}"}, status=status.HTTP_400_BAD_REQUEST)


        if not input_serializer.is_valid():
            return Response(input_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        validated_data = input_serializer.validated_data
        reference_text = validated_data['reference_text']
        speaking_text_id = validated_data.get('speaking_text_id') # Optional
        user = request.user

        # --- 2. Process Audio File (Save Temporarily and Convert to WAV) ---
        temp_dir = None
        wav_path = None
        try:
            # Tạo thư mục tạm an toàn
            temp_dir = tempfile.mkdtemp(prefix="speakpro_assess_")
            # Lưu file gốc tạm thời
            original_filename = audio_file.name
            # Sanitize filename to avoid issues:
            safe_filename = re.sub(r'[^\w\.-]', '_', original_filename)
            original_extension = os.path.splitext(safe_filename)[1].lower()
            temp_original_path = os.path.join(temp_dir, f"input{original_extension}")

            with open(temp_original_path, 'wb+') as destination:
                for chunk in audio_file.chunks():
                    destination.write(chunk)

            # Chuyển đổi sang WAV (mono, 16kHz)
            wav_filename = "processed_audio.wav"
            wav_path = os.path.join(temp_dir, wav_filename)

            print(f"Processing audio: {temp_original_path} -> {wav_path}")
            sound = AudioSegment.from_file(temp_original_path) # pydub tự phát hiện format
            sound = sound.set_channels(1) # Đảm bảo mono
            sound = sound.set_frame_rate(16000) # Chuẩn hóa sample rate
            # Export WAV
            sound.export(wav_path, format="wav")
            print("Conversion to WAV successful.")

        except Exception as e:
            print(f"Error processing audio file: {e}")
            # Cleanup if temp dir was created
            if temp_dir and os.path.exists(temp_dir):
                shutil.rmtree(temp_dir, ignore_errors=True)
            return Response({"error": f"Failed to process audio file. Ensure it is a valid audio format."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # --- 3. Perform Pronunciation Assessment ---
        assessment_result_data = None
        try:
            # --- !!! CHỌN PHƯƠNG THỨC ĐÁNH GIÁ TẠI ĐÂY !!! ---

            # >>> Option 1: Sử dụng Azure (Recommended) <<<
            # try:
            #     assessment_result_data = call_azure_pronunciation_assessment(wav_path, reference_text)
            #     if assessment_result_data:
            #         # Xử lý thêm kết quả Azure nếu cần (vd: tạo errors_for_highlighting)
            #         assessment_result_data["errors"] = self.extract_highlight_errors_from_azure(assessment_result_data, reference_text) # Sử dụng key 'errors'
            # except ValueError as azure_config_error: # Catch config error from placeholder
            #      print(f"Azure Config Error: {azure_config_error}")
            #      return Response({"error": "Pronunciation assessment service is not configured."}, status=status.HTTP_501_NOT_IMPLEMENTED)
            # except Exception as azure_error:
            #      print(f"Azure Assessment Error: {azure_error}")
            #      # Rethrow specific errors handled below or raise a generic one
            #      raise azure_error


            # >>> Option 2: Sử dụng Mô Phỏng (Currently active) <<<
            assessment_result_data = simulate_pronunciation_assessment(wav_path, reference_text)


            # >>> Option 3: Tích hợp Whisper + Logic riêng (Tự viết) <<<
            # transcribed_text = call_whisper_stt(wav_path) # Viết hàm này
            # assessment_result_data = compare_and_score(transcribed_text, reference_text, wav_path) # Logic riêng


            if not assessment_result_data:
                 # Assessment function should ideally raise exceptions on failure
                 raise Exception("Assessment function returned no result unexpectedly.")

        except sr.UnknownValueError as e:
             print(f"Assessment Error: Could not understand audio: {e}")
             # Trả về lỗi rõ ràng cho frontend
             return Response({
                 "error": "Could not understand the speech in the audio file. Please try speaking more clearly.",
                 "details": str(e)
                 }, status=status.HTTP_400_BAD_REQUEST)
        except sr.RequestError as e:
             print(f"Assessment Error: Speech service unavailable: {e}")
             return Response({
                 "error": "The speech recognition service is currently unavailable. Please try again later.",
                 "details": str(e)
                 }, status=status.HTTP_503_SERVICE_UNAVAILABLE)
        except Exception as e:
            # Catch-all for other assessment errors
            print(f"Unexpected error during pronunciation assessment: {e}")
            return Response({
                "error": "An unexpected error occurred during pronunciation assessment.",
                "details": str(e) # Gửi chi tiết lỗi (cân nhắc vấn đề bảo mật)
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        finally:
            # --- 4. Cleanup Temporary Files ---
            if temp_dir and os.path.exists(temp_dir):
                try:
                    shutil.rmtree(temp_dir, ignore_errors=True) # ignore_errors để không crash nếu xóa lỗi
                    print(f"Temporary directory {temp_dir} cleaned up.")
                except Exception as cleanup_error:
                    # Log lỗi cleanup nhưng không ảnh hưởng response chính
                    print(f"Warning: Error cleaning up temp directory {temp_dir}: {cleanup_error}")

        # --- 5. Save Practice Log ---
        try:
            speaking_text_instance = None
            if speaking_text_id:
                try:
                    speaking_text_instance = SpeakingText.objects.get(id=speaking_text_id)
                except SpeakingText.DoesNotExist:
                    print(f"Warning: SpeakingText with id={speaking_text_id} not found for logging.")

            # Chuẩn bị dữ liệu chi tiết để lưu vào JSONField
            log_details = {
                "pronunciation_score": assessment_result_data.get('pronunciation_score'),
                "accuracy_score": assessment_result_data.get('accuracy_score'),
                "fluency_score": assessment_result_data.get('fluency_score'),
                "completeness_score": assessment_result_data.get('completeness_score'),
                "errors_for_highlighting": assessment_result_data.get('errors', []) # Dùng key 'errors' từ result
                # Thêm 'words' từ Azure nếu có
                # "words": assessment_result_data.get('words')
            }

            log_entry = UserPracticeLog.objects.create(
                user=user,
                speaking_text=speaking_text_instance,
                reference_text=reference_text, # Lưu câu gốc đã dùng
                transcribed_text=assessment_result_data.get('transcribed_text'), # Lưu kết quả STT
                score=assessment_result_data.get('pronunciation_score'), # Lưu điểm tổng thể
                details=log_details # Lưu cấu trúc chi tiết
            )
            print(f"Practice log saved with ID: {log_entry.id}")
        except Exception as log_error:
            # Log lỗi nghiêm trọng nếu việc lưu log thất bại
            print(f"CRITICAL: Error saving practice log: {log_error}")
            # Cân nhắc có nên trả lỗi 500 ở đây không nếu việc lưu log là bắt buộc

        # --- 6. Prepare and Return Response using Serializer ---
        # Dữ liệu đã có cấu trúc gần giống PronunciationAssessmentResultSerializer
        # Chỉ cần đảm bảo các key khớp (ví dụ: 'errors' thay vì 'errors_for_highlighting')
        response_data = assessment_result_data # Dữ liệu từ hàm assessment (đã bao gồm 'errors')

        output_serializer = PronunciationAssessmentResultSerializer(data=response_data)
        if output_serializer.is_valid():
             return Response(output_serializer.validated_data, status=status.HTTP_200_OK)
        else:
             # Lỗi này chỉ xảy ra nếu hàm assessment trả về sai cấu trúc so với serializer
             print(f"CRITICAL: Output serializer errors: {output_serializer.errors}")
             print(f"Data passed to output serializer: {response_data}")
             # Trả về lỗi server vì backend không tạo được response hợp lệ
             return Response(
                 {"error": "Failed to serialize assessment results.", "serializer_errors": output_serializer.errors},
                 status=status.HTTP_500_INTERNAL_SERVER_ERROR
             )

    # Helper function placeholder (nếu dùng Azure)
    # def extract_highlight_errors_from_azure(self, azure_result, reference_text):
    #     errors_for_highlighting = []
    #     # ... (Logic map offset/duration thành start/end index) ...
    #     print("Placeholder: Azure error extraction not implemented.")
    #     return errors_for_highlighting


# ==============================================================================
#                         CRUD OPERATIONS - USERS (Admin)
# ==============================================================================
class UserListView(generics.ListAPIView): # Chỉ List
    queryset = User.objects.all().order_by('id')
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser] # Chỉ Admin xem danh sách user

# User Create/Update/Delete nên được quản lý cẩn thận hơn là API CRUD đơn giản
# Ví dụ: dùng RegisterView cho tạo user, và cần API riêng cho admin quản lý user
class UserDetailView(generics.RetrieveUpdateDestroyAPIView): # Cho phép Admin RUD user cụ thể
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]
    lookup_field = 'pk' # Hoặc 'id'
