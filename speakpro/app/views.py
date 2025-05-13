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

# App Imports (Models & Serializers)
from .models import (
    Genre, SpeakingText, Audio, UserPracticeLog, Level, SpeakingResult, UserAudio # Combined models
)
from .serializers import (
    GenreSerializer, SpeakingTextSerializer, AudioSerializer,
    ResetPasswordSerializer, UserPracticeLogSerializer, UserSerializer, 
    LevelSerializer, UserAudioSerializer 
)

# NOTE: Specific utility/library imports are placed within their functional sections below for clarity.


# ==============================================================================
#                                  HOME VIEW
# ==============================================================================


def home(request):
    return HttpResponse("Speakpro")

# ==============================================================================
#                         AUTHENTICATION & USER MANAGEMENT VIEWS 
# ==============================================================================
# Imports required for this section are already in COMMON IMPORTS
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
class RegisterView(APIView):
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

        # Check if username already exists (added for robustness, User model requires unique username)
        if User.objects.filter(username=username).exists():
             return Response({'error': 'Username already exists!'}, status=status.HTTP_400_BAD_REQUEST)

        # Create the new user
        user = User.objects.create_user(
            username=username,  # Username is now the unique identifier
            email=email,  # Email used for login and notifications
            password=password
        )

        return Response({'message': 'User registered successfully!'}, status=status.HTTP_201_CREATED)


class LoginView(APIView):
    def post(self, request):
        data = request.data
        username = data.get('username')
        password = data.get('password')

        try:
            # Find user by username
            user = User.objects.get(username=username)

            # Authenticate user with username and password
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
            return Response({'message': 'User with this username does not exist!'},
                            status=status.HTTP_401_UNAUTHORIZED)

class LogoutView(APIView):
    def post(self, request):
        try:
            # Get refresh token from request
            refresh_token = request.data.get('refresh_token')
            if not refresh_token:
                 return Response({"error": "Refresh token is required"}, status=status.HTTP_400_BAD_REQUEST)
            token = RefreshToken(refresh_token)
            token.blacklist()  # Add token to blacklist

            return Response({"message": "Logged out successfully"}, status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            # Catch specific exceptions like TokenError if possible
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class ForgotPasswordView(APIView):
    def post(self, request):
        email = request.data.get('email')
        if not email:
            return Response({'error': 'Email is required!'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            # Return success-like message even if user doesn't exist to avoid email enumeration
            return Response({'message': 'If an account with this email exists, a confirmation code has been sent.'}, status=status.HTTP_200_OK)
            # Or be explicit: return Response({'error': 'User with this email does not exist!'}, status=status.HTTP_404_NOT_FOUND)

        # Generate a confirmation code
        confirmation_code = ''.join(random.choices(string.ascii_letters + string.digits, k=6))

        # Store the confirmation code in cache with a timeout (e.g., 10 minutes)
        cache.set(f"password_reset_code_{email}", confirmation_code, timeout=600)

        try:
            send_mail(
                subject="Password Reset Confirmation Code - Speakpro", # Updated subject
                message=f"Hello {user.username or user.first_name or 'User'},\n\nYour confirmation code is: {confirmation_code}\nUse this code to reset your password. It will expire in 10 minutes.",
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[email],
                fail_silently=False,
            )
            return Response({'message': 'Confirmation code sent to your email!'}, status=status.HTTP_200_OK)
        except Exception as e:
            # Log the error e for debugging
            print(f"Error sending password reset email to {email}: {e}")
            return Response({'error': 'Failed to send email. Please try again later.'}, # Removed details from response 'details': str(e)
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

        if not cached_code:
            return Response({'error': 'Expired confirmation code! Please request a new one.'}, status=status.HTTP_400_BAD_REQUEST)
        if cached_code != confirmation_code:
             return Response({'error': 'Invalid confirmation code!'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            # This case should ideally not happen if ForgotPasswordView checks, but good to have.
            return Response({'error': 'User with this email does not exist!'}, status=status.HTTP_404_NOT_FOUND)

        # Update the password
        user.set_password(new_password)
        user.save()

        # Clear the confirmation code from cache
        cache.delete(f"password_reset_code_{email}")

        return Response({'message': 'Password has been reset successfully!'}, status=status.HTTP_200_OK)

def is_admin(user):
    return user.is_authenticated and user.is_superuser  

@permission_classes([IsAuthenticated])
@api_view(['GET'])
def admin_dashboard(request):
    if is_admin(request.user):
        return Response({'message': 'Welcome Admin!'}, status=status.HTTP_200_OK)
    return Response({'error': 'Unauthorized'}, status=status.HTTP_403_FORBIDDEN)

# ==============================================================================
#                         USER PROGRESS & HISTORY VIEWS 
# ==============================================================================
# Imports required for this section are already in COMMON IMPORTS

class UserPracticeLogView(ListCreateAPIView):
    """
    API endpoint for:
    - GET: Fetching the practice history of the logged-in user.
    - POST: Recording a new practice session for the logged-in user.

    Requires:
    - speaking_text_id: ID of the practiced SpeakingText.
    - score: Achieved score.
    - details: JSON/text details (optional).
    """
    serializer_class = UserPracticeLogSerializer
    permission_classes = [IsAuthenticated] # Requires authentication

    def get_queryset(self):
        """
        Return only the history for the currently authenticated user.
        Order by the most recent practice date.
        """
        user = self.request.user
        # Use select_related to optimize queries by fetching related user, speaking_text, and genre info together
        return UserPracticeLog.objects.filter(user=user).select_related(
            'user', 'speaking_text', 'speaking_text__genre', 'speaking_text__level' # Added level
        ).order_by('-practice_date') # Order by most recent

    def perform_create(self, serializer):
        """
        Automatically assign the logged-in user to the 'user' field when creating a new log.
        """
        serializer.save(user=self.request.user)

# ==============================================================================
#                            DASHBOARD & STATS VIEWS 
# ==============================================================================
# Imports required for this section are already in COMMON IMPORTS

User = get_user_model()

class DashboardStatsView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request, format=None):
        now = timezone.now()
        last_7_days = now - timedelta(days=7)

        # Tổng người dùng
        total_users = User.objects.count()

        # Nội dung đang hoạt động (ví dụ: status=True)
        active_content = SpeakingText.objects.filter(is_active=True).count()

        # Tổng số bản ghi luyện tập
        total_reports = UserPracticeLog.objects.count()

        # Tính phần trăm người dùng hoạt động 7 ngày qua
        active_user_ids = UserPracticeLog.objects.filter(
            practice_date__gte=last_7_days
        ).values_list('user_id', flat=True).distinct()
        engagement_percent = round((active_user_ids.count() / total_users) * 100) if total_users > 0 else 0

        # Hoạt động từng ngày
        daily_activity = UserPracticeLog.objects.filter(
            practice_date__gte=last_7_days
        ).extra({'day': "DATE(practice_date)"}).values('day').annotate(count=Count('id')).order_by('day')

        # Chuyển đổi sang format frontend cần
        daily_user_activity = [
            {'day': record['day'].strftime('%a'), 'value': record['count']}
            for record in daily_activity
        ]

        # Nội dung theo thể loại
        category_usage = (
            SpeakingText.objects.values('genre__name')  # genre là FK
            .annotate(count=Count('id'))
            .order_by('-count')
        )
        content_usage_by_category = [
            {'category': item['genre__name'], 'value': item['count']}
            for item in category_usage
        ]

        return Response({
            'total_users': total_users,
            'active_content': active_content,
            'total_reports': total_reports,
            'user_engagement_percent': engagement_percent,
            'daily_user_activity': daily_user_activity,
            'content_usage_by_category': content_usage_by_category
        })


# ==============================================================================
#                         SPEAKPRO CORE API VIEWS (Combined)
# ==============================================================================
# Imports required for this section are already in COMMON IMPORTS

# API to get list of all genres 
class GenreListView(APIView):
    def get(self, request):
        genres = Genre.objects.all()
        serializer = GenreSerializer(genres, many=True)
        return Response(serializer.data)

# API to get genre by ID 
class GenreDetailView(APIView):
    def get(self, request, pk):
        try:
            genre = Genre.objects.get(pk=pk)
        except Genre.DoesNotExist:
            return Response({"error": "Genre not found"}, status=status.HTTP_404_NOT_FOUND) # Added error msg
        serializer = GenreSerializer(genre)
        return Response(serializer.data)

# API to get list of all Speaking Texts 
class SpeakingTextListView(APIView):
    def get(self, request):
        # Optimize by prefetching related objects if needed frequently in serialization
        texts = SpeakingText.objects.select_related('genre', 'level').all()
        serializer = SpeakingTextSerializer(texts, many=True, context={'request': request}) # Pass request context for potential hyperlinking
        return Response(serializer.data)

# API to get Speaking Text by ID 
class SpeakingTextDetailView(APIView):
    def get(self, request, pk):
        try:
            # Optimize by prefetching related objects
            text = SpeakingText.objects.select_related('genre', 'level').get(pk=pk)
        except SpeakingText.DoesNotExist:
            return Response({"error": "Speaking text not found"}, status=status.HTTP_404_NOT_FOUND) # Added error msg
        serializer = SpeakingTextSerializer(text, context={'request': request}) # Pass context
        return Response(serializer.data)

# API to filter Speaking Texts by genre and/or level 
class SpeakingTextFilterAPIView(generics.ListAPIView):
    serializer_class = SpeakingTextSerializer

    def get_queryset(self):
        """
        Filter the list of speaking texts by genre and level query parameters.
        """
        # Start with all texts, prefetch related models for efficiency
        queryset = SpeakingText.objects.select_related('genre', 'level').all()

        # Filter by genre if 'genre' query parameter is provided
        genre_id = self.request.query_params.get('genre', None)
        if genre_id:
            queryset = queryset.filter(genre_id=genre_id)

        # Filter by level if 'level' query parameter is provided
        level_id = self.request.query_params.get('level', None)
        if level_id:
            queryset = queryset.filter(level_id=level_id)

        return queryset

# API View for searching Speaking Texts (Topics) by title or genre name 
class SpeakingTextSearchView(ListAPIView):
    serializer_class = SpeakingTextSerializer
    # Use DRF's SearchFilter backend
    filter_backends = [SearchFilter]
    # Specify fields to search against
    # 'title': search in SpeakingText's title field
    # 'genre__name': search in the related Genre's name field (using '__' for related fields)
    # Default search is case-insensitive 'contains'. Prefixes like '^', '=', '@', '$' can modify search behavior.
    search_fields = ['title', 'genre__name', 'level__name'] # Added level name search
    queryset = SpeakingText.objects.select_related('genre', 'level').all() # Optimized query

# API to get list of all audios 
class AudioListView(APIView):
    def get(self, request):
        audios = Audio.objects.all()
        serializer = AudioSerializer(audios, many=True, context={'request': request}) # Pass context
        return Response(serializer.data)

# API to get audio detail (URL) by ID 
class AudioDetailView(APIView):
    def get(self, request, pk):
        try:
            # Get the Audio object from the database by primary key (pk)
            audio = Audio.objects.get(pk=pk)
        except Audio.DoesNotExist:
            return Response({"error": "Audio not found."}, status=status.HTTP_404_NOT_FOUND)

        # Ensure the audio file exists
        if not audio.audio_file:
            # This case might indicate a data integrity issue
            return Response({"error": "Audio record exists but the file is missing."}, status=status.HTTP_404_NOT_FOUND)

        try:
            # Get the URL of the audio file (FileField provides a .url attribute)
            audio_url = audio.audio_file.url
            # Construct the full absolute URL using the request context
            full_audio_url = request.build_absolute_uri(audio_url)
            return Response({"audio_url": full_audio_url}, status=status.HTTP_200_OK)
        except Exception as e:
            # Handle potential errors during URL building
            print(f"Error generating audio URL for pk={pk}: {e}")
            return Response({"error": "Could not generate audio URL."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# ==============================================================================
#                         AUDIO PROCESSING & SUBMISSION VIEWS 
# ==============================================================================

# Specific Imports for this section
import speech_recognition as sr
from pydub import AudioSegment
from .utils.score import calculate_score # Assuming this exists in utils/score.py
from .utils.audio_converter import convert_webm_to_mp3 # Assuming this exists in utils/audio_converter.py

# Helper function to split audio (Consider moving to utils if reused elsewhere)
def split_audio_to_chunks(audio_path, chunk_length_ms=15000):
    """Splits a WAV audio file into chunks of specified length."""
    try:
        audio = AudioSegment.from_wav(audio_path)
        chunks = [audio[i:min(i + chunk_length_ms, len(audio))] for i in range(0, len(audio), chunk_length_ms)]
        return chunks
    except Exception as e:
        print(f"Error splitting audio {audio_path}: {e}")
        return [] # Return empty list on error

# API view for uploading user audio (e.g., WebM) and converting it to MP3 
@csrf_exempt # Use SessionAuthentication/TokenAuthentication in DRF instead of CSRF exempt if possible
@api_view(['POST'])
def upload_user_audio(request):
    audio_file = request.FILES.get('audio')
    # It's better to use the authenticated user: user = request.user
    # For testing/demo, we might get a specific user or allow anonymous uploads
    user = request.user if request.user.is_authenticated else None
    if not user:
         # If authentication is required, enforce it here or via permissions
         # For now, let's fallback to a test user if not logged in (NOT RECOMMENDED FOR PRODUCTION)
         try:
             user = User.objects.get(username='tranv') # Example test user
         except User.DoesNotExist:
             return Response({"error": "Test user 'tranv' not found and no user logged in."}, status=status.HTTP_400_BAD_REQUEST)

    if not audio_file:
        return Response({"error": "No audio file provided ('audio' field)"}, status=status.HTTP_400_BAD_REQUEST)

    # Validate file type/size if necessary
    # E.g., if not audio_file.name.endswith('.webm'): return Response(...)

    try:
        # Save the original audio file (.webm)
        user_audio = UserAudio.objects.create(user=user, audio_file=audio_file)
        original_serializer = UserAudioSerializer(user_audio, context={'request': request})

        # Define paths for conversion
        input_path = user_audio.audio_file.path
        filename_wo_ext = os.path.splitext(os.path.basename(input_path))[0]
        # Place converted files in a specific subfolder within MEDIA_ROOT
        converted_dir_name = 'converted_audio'
        output_dir = os.path.join(settings.MEDIA_ROOT, converted_dir_name)
        os.makedirs(output_dir, exist_ok=True) # Create directory if it doesn't exist
        output_path = os.path.join(output_dir, f"{filename_wo_ext}.mp3")

        # Convert WebM -> MP3 using the utility function
        success = convert_webm_to_mp3(input_path, output_path)
        if not success:
            user_audio.delete() # Clean up the created UserAudio record if conversion fails
            return Response({"error": "Failed to convert audio."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # Construct the relative URL for the converted MP3 file
        mp3_relative_path = os.path.join(converted_dir_name, f"{filename_wo_ext}.mp3")
        # Construct the absolute URL using MEDIA_URL
        mp3_absolute_url = request.build_absolute_uri(os.path.join(settings.MEDIA_URL, mp3_relative_path))


        return Response({
            'message': 'File uploaded and converted successfully.',
            'original_audio_url': original_serializer.data['audio_file'], # URL from serializer
            'converted_audio_url': mp3_absolute_url
        }, status=status.HTTP_201_CREATED)

    except Exception as e:
        # Log the exception
        print(f"Error during audio upload/conversion: {e}")
        # Clean up UserAudio record if created before the error
        if 'user_audio' in locals() and user_audio.pk:
             try:
                 user_audio.delete()
             except: pass # Ignore cleanup errors
        return Response({"error": "An unexpected error occurred during processing."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# API view for submitting speaking practice audio, comparing with text, and getting score 
class SubmitSpeakingAPIView(APIView):
    permission_classes = [IsAuthenticated] # Usually requires user context

    def post(self, request):
        audio_file = request.FILES.get("audio_file") # Expecting the audio file in the request
        speaking_text_id = request.data.get("speaking_text_id") # Expecting the ID of the reference text
        user = request.user # Get the authenticated user

        if not audio_file or not speaking_text_id:
            return Response({"error": "Missing 'audio_file' or 'speaking_text_id'."}, status=status.HTTP_400_BAD_REQUEST)

        # --- 1. Save and Convert Audio ---
        temp_dir = os.path.join(settings.MEDIA_ROOT, 'temp_submissions')
        os.makedirs(temp_dir, exist_ok=True)
        # Use a unique filename to avoid collisions
        temp_filename = f"{user.id}_{speaking_text_id}_{timezone.now().strftime('%Y%m%d%H%M%S')}.webm"
        temp_path = os.path.join(temp_dir, temp_filename)

        # Save the uploaded file temporarily
        try:
            with default_storage.open(temp_path, 'wb+') as destination:
                for chunk in audio_file.chunks():
                    destination.write(chunk)
        except Exception as e:
            print(f"Error saving temporary audio file: {e}")
            return Response({"error": "Failed to save uploaded audio file."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


        # Convert webm -> wav for speech recognition
        wav_path = temp_path.replace('.webm', '.wav')
        try:
            sound = AudioSegment.from_file(temp_path, format="webm") # Specify input format if needed
            sound.export(wav_path, format="wav")
        except Exception as e:
            print(f"Error converting webm to wav: {e}")
            # Cleanup temp webm file
            if os.path.exists(temp_path): os.remove(temp_path)
            return Response({"error": "Failed to convert audio to WAV format."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


        # --- 2. Speech Recognition ---
        recognizer = sr.Recognizer()
        recognized_text = ""
        try:
            # Use chunking for potentially long audio files
            chunks = split_audio_to_chunks(wav_path, chunk_length_ms=15000) # 15 seconds per chunk
            if not chunks: # Handle error from split_audio_to_chunks
                 raise Exception("Audio splitting failed.")

            for i, chunk in enumerate(chunks):
                # Process each chunk
                chunk_path = f"{wav_path}_chunk_{i}.wav"
                chunk.export(chunk_path, format="wav")

                with sr.AudioFile(chunk_path) as source:
                    audio_data = recognizer.record(source) # Read the chunk audio data
                    try:
                        # Recognize speech using Google Web Speech API
                        text = recognizer.recognize_google(audio_data, language="en-US") # Specify language
                        recognized_text += text + " " # Append recognized text
                    except sr.UnknownValueError:
                        print(f"[Warning] Chunk {i}: Google Speech Recognition could not understand audio.")
                        # Optionally append a placeholder or log this missing part
                    except sr.RequestError as e:
                        print(f"[Error] Chunk {i}: Could not request results from Google Speech Recognition service; {e}")
                        # Decide how to handle API errors (e.g., retry, fail, partial result)
                        # For now, we'll continue, potentially resulting in incomplete text

                # Clean up chunk file
                if os.path.exists(chunk_path): os.remove(chunk_path)

            user_text_raw = recognized_text.strip()
            if not user_text_raw:
                 # Handle case where nothing was recognized
                 raise sr.UnknownValueError("No speech recognized from the audio.")


        except sr.UnknownValueError:
            # Cleanup temp files
            if os.path.exists(temp_path): os.remove(temp_path)
            if os.path.exists(wav_path): os.remove(wav_path)
            return Response({"error": "Could not understand audio or no speech detected."}, status=status.HTTP_400_BAD_REQUEST)
        except sr.RequestError as e:
            # Cleanup temp files
            if os.path.exists(temp_path): os.remove(temp_path)
            if os.path.exists(wav_path): os.remove(wav_path)
            return Response({"error": f"Speech recognition service error: {e}"}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
        except Exception as e: # Catch other potential errors during processing
             print(f"Error during speech recognition: {e}")
             # Cleanup temp files
             if os.path.exists(temp_path): os.remove(temp_path)
             if os.path.exists(wav_path): os.remove(wav_path)
             return Response({"error": "An unexpected error occurred during speech recognition."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # --- 3. Get Original Text ---
        try:
            speaking_text = SpeakingText.objects.get(id=speaking_text_id)
            # Decode the original content (assuming it's stored correctly)
            # The original view1 had hex decoding, let's assume it's just UTF-8 text
            original_text = speaking_text.content # Adjust if decoding (e.g., hex, base64) is needed
            # If hex encoded as in view1:
            # try:
            #     original_bytes = bytes.fromhex(speaking_text.content) # Assuming content is hex string
            #     original_text = original_bytes.decode("utf-8")
            # except (ValueError, TypeError, AttributeError, UnicodeDecodeError) as decode_error:
            #     print(f"Error decoding original text content for ID {speaking_text_id}: {decode_error}")
            #     return Response({"error": "Could not decode the original text content."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        except SpeakingText.DoesNotExist:
            # Cleanup temp files
            if os.path.exists(temp_path): os.remove(temp_path)
            if os.path.exists(wav_path): os.remove(wav_path)
            return Response({"error": "Reference speaking text not found."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e: # Catch other errors getting/decoding text
             print(f"Error retrieving/processing original text {speaking_text_id}: {e}")
             # Cleanup temp files
             if os.path.exists(temp_path): os.remove(temp_path)
             if os.path.exists(wav_path): os.remove(wav_path)
             return Response({"error": "Failed to retrieve or process the reference text."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # --- 4. Calculate Score ---
        try:
            # Call your scoring function
            result = calculate_score(user_text_raw, original_text) # Assumes calculate_score returns a dict like {'score': ..., 'details': ...}
        except Exception as e:
            print(f"Error calculating score: {e}")
            # Cleanup temp files
            if os.path.exists(temp_path): os.remove(temp_path)
            if os.path.exists(wav_path): os.remove(wav_path)
            return Response({"error": "Failed to calculate the score."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # --- 5. Save Result (Optional) & Cleanup ---
        try:
            # Optionally save the practice log (can use the UserPracticeLogView logic or save directly)
             UserPracticeLog.objects.create(
                 user=user,
                 speaking_text=speaking_text,
                 score=result.get('score', 0), # Get score from result dict, default to 0
                 details=result.get('details', None) # Get details if available
                 # user_audio_path=wav_path # Optionally store path to the processed audio
             )
             # Consider saving the raw recognized text as well if needed for review
             # SpeakingResult.objects.create(...) # If you have a separate model like view1

        except Exception as e:
            print(f"Error saving practice log: {e}")
            # Don't fail the request if logging fails, but log the error

        # Cleanup temporary files
        finally: # Ensure cleanup happens even if logging fails
             if os.path.exists(temp_path): os.remove(temp_path)
             if os.path.exists(wav_path): os.remove(wav_path)


        # --- 6. Return Result ---
        # Add the recognized text to the response for the user to see
        response_data = {
            "recognized_text": user_text_raw,
            "original_text": original_text, # Maybe return original text for comparison on frontend
            "score_result": result # Contains score and potentially detailed analysis
        }
        return Response(response_data, status=status.HTTP_200_OK)


# ==============================================================================
#                         CRUD OPERATIONS - SPEAKING TEXTS 
# ==============================================================================
# Imports required for this section are already in COMMON IMPORTS

# API to create a new SpeakingText 
class SpeakingTextCreateAPIView(APIView):
    permission_classes = [IsAdminUser] # Typically restricted to admins

    def post(self, request):
        serializer = SpeakingTextSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            # The serializer handles nested relationships (Genre, Level) if configured correctly
            # Or you extract IDs/names and fetch/create Genre/Level objects manually before saving
            # Example: Manual handling (if serializer doesn't handle nested creation)
            # genre_data = request.data.get('genre') # Could be ID or dict {'name': '...'}
            # level_data = request.data.get('level') # Could be ID or dict {'name': '...'}
            # ... logic to get_or_create genre and level objects ...
            # serializer.save(genre=genre_obj, level=level_obj)
            try:
                 serializer.save()
                 return Response(serializer.data, status=status.HTTP_201_CREATED)
            except Exception as e:
                 # Handle potential errors during save (e.g., database constraints)
                 print(f"Error saving SpeakingText: {e}")
                 return Response({"error": f"Failed to save SpeakingText: {e}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# API to update an existing SpeakingText 
class SpeakingTextUpdateAPIView(generics.UpdateAPIView):
    queryset = SpeakingText.objects.all()
    serializer_class = SpeakingTextSerializer
    permission_classes = [IsAdminUser] # Typically restricted to admins
    lookup_field = 'id' # Use 'id' to find the object (can change to 'pk')

# API to delete a SpeakingText 
class SpeakingTextDeleteAPIView(generics.DestroyAPIView):
    queryset = SpeakingText.objects.all()
    serializer_class = SpeakingTextSerializer # Serializer used for potential response (usually none on delete)
    permission_classes = [IsAdminUser] # Typically restricted to admins
    lookup_field = 'id' # Use 'id' to find the object

# ==============================================================================
#                         CRUD OPERATIONS - USERS 
# ==============================================================================
# Imports required for this section are already in COMMON IMPORTS

# API to list users 
class UserListView(generics.ListAPIView):
    queryset = User.objects.all().order_by('id') # Get all users
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser] # Listing all users typically requires admin rights

# API to create a user 
# Note: This might bypass standard Django user creation signals/password hashing if UserSerializer is basic.
# Consider using the RegisterView above or ensuring UserSerializer handles password hashing correctly.
class UserCreateAPIView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer # Ensure this serializer handles password hashing!
    permission_classes = [IsAdminUser] # Creating users directly often requires admin rights

# API to update a user 
class UserUpdateAPIView(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer # Ensure this handles password changes securely if allowed
    permission_classes = [IsAdminUser] # Or allow users to update their own profiles
    lookup_field = 'id' # Find user by id

# API to delete a user 
class UserDeleteAPIView(generics.DestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser] # Deleting users typically requires admin rights
    lookup_field = 'id' # Find user by id


# ==============================================================================
#                                 LEVELS API 
# ==============================================================================
# Imports required for this section are already in COMMON IMPORTS

# API to list all available Levels 
class LevelListAPIView(generics.ListAPIView):
    queryset = Level.objects.all()  # Lấy tất cả các level
    serializer_class = LevelSerializer  # Sử dụng LevelSerializer để trả về dữ liệu


# ==============================================================================
#                                 CHALENGES API 
# ==============================================================================

from rest_framework import viewsets, mixins 
from rest_framework.decorators import action 
from django.db.models import Window, F
from django.db.models.functions import Rank
from django.shortcuts import get_object_or_404 
from .models import ( 
    ChallengeCategory, Challenge, ChallengeExercise,
    UserChallengeAttempt, UserChallengeExerciseAttempt, UserChallengeStreak,
    Achievement, UserAchievement, UserPracticeLog, SpeakingText 
)
from .serializers import ( 
    ChallengeCategorySerializer, ChallengeSerializer, ChallengeExerciseSerializer,
    UserChallengeAttemptSerializer, UserChallengeExerciseAttemptSerializer,
    UserChallengeStreakSerializer, AchievementSerializer, UserAchievementSerializer,
    ChallengeLeaderboardEntrySerializer 
)
class ChallengeCategoryViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint for listing and retrieving Challenge Categories.
    """
    queryset = ChallengeCategory.objects.all()
    serializer_class = ChallengeCategorySerializer
    permission_classes = [IsAuthenticated] 


class ChallengeViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint for listing and retrieving Challenges.
    Includes user-specific progress if authenticated.
    """
    queryset = Challenge.objects.filter(is_active=True).prefetch_related(
        'exercises__speaking_text', 'level', 'category'
    ) # Chỉ lấy challenge active
    serializer_class = ChallengeSerializer
    permission_classes = [IsAuthenticated] 

    def get_serializer_context(self):
        # Truyền request vào context để serializer có thể lấy user
        return {'request': self.request, 'format': self.format_kwarg, 'view': self}

    @action(detail=True, methods=['post'], url_path='start')
    def start_challenge(self, request, pk=None):
        """
        Allows an authenticated user to start a challenge.
        Creates a UserChallengeAttempt if one doesn't exist.
        """
        challenge = self.get_object()
        user = request.user

        if not challenge.get_is_currently_active:
            return Response({"error": "This challenge is not currently active."}, status=status.HTTP_400_BAD_REQUEST)

        attempt, created = UserChallengeAttempt.objects.get_or_create(
            user=user,
            challenge=challenge,
            defaults={'status': 'in_progress', 'started_at': timezone.now()}
        )

        if not created and attempt.status == 'not_started': # Nếu đã có nhưng chưa bắt đầu
            attempt.status = 'in_progress'
            attempt.started_at = timezone.now() # Cập nhật lại thời gian bắt đầu
            attempt.save()
        
        # Tạo các UserChallengeExerciseAttempt nếu chưa có
        exercises = challenge.exercises.all()
        for exercise in exercises:
            UserChallengeExerciseAttempt.objects.get_or_create(
                user_challenge_attempt=attempt,
                challenge_exercise=exercise
            )

        serializer = UserChallengeAttemptSerializer(attempt, context=self.get_serializer_context())
        return Response(serializer.data, status=status.HTTP_200_OK if not created else status.HTTP_201_CREATED)

    @action(detail=True, methods=['get'], url_path='exercises')
    def list_exercises_with_status(self, request, pk=None):
        """
        List exercises for a specific challenge, including the current user's completion status for each.
        """
        challenge = self.get_object()
        user = request.user
        
        try:
            user_attempt = UserChallengeAttempt.objects.get(user=user, challenge=challenge)
        except UserChallengeAttempt.DoesNotExist:
            # Nếu user chưa bắt đầu challenge, có thể trả về danh sách exercise không có status
            # Hoặc yêu cầu user start challenge trước
             return Response({"error": "You have not started this challenge yet. Please start the challenge first."}, status=status.HTTP_400_BAD_REQUEST)

        # Lấy tất cả các UserChallengeExerciseAttempt của user cho challenge này
        exercise_attempts = UserChallengeExerciseAttempt.objects.filter(
            user_challenge_attempt=user_attempt
        ).select_related('challenge_exercise__speaking_text', 'user_practice_log')

        # Serialize dữ liệu
        # Cần một serializer có thể kết hợp ChallengeExercise và UserChallengeExerciseAttempt
        
        # Tạm thời trả về danh sách UserChallengeExerciseAttemptSerializer
        # Frontend sẽ cần map với danh sách exercises từ ChallengeSerializer nếu cần
        # Hoặc chúng ta tạo một response tùy chỉnh ở đây
        
        data = []
        all_challenge_exercises = challenge.exercises.order_by('order').select_related('speaking_text__genre', 'speaking_text__level')

        for ch_exercise in all_challenge_exercises:
            exercise_data = ChallengeExerciseSerializer(ch_exercise).data
            attempt_data = None
            try:
                ex_attempt = exercise_attempts.get(challenge_exercise=ch_exercise)
                attempt_data = UserChallengeExerciseAttemptSerializer(ex_attempt).data
            except UserChallengeExerciseAttempt.DoesNotExist:
                # User chưa làm bài này, có thể tạo một entry rỗng cho is_completed=false
                pass 
            
            exercise_data['user_attempt_details'] = attempt_data
            data.append(exercise_data)
            
        return Response(data)


    @action(detail=True, methods=['get'], url_path='leaderboard')
    def leaderboard(self, request, pk=None):
        """
        Get leaderboard for a challenge.
        Lists top users by points_earned and completion_time.
        """
        challenge = self.get_object()
        # Lấy các attempt đã hoàn thành, sắp xếp theo điểm, sau đó theo thời gian hoàn thành
        # Giới hạn ví dụ 10 người đầu
        leaderboard_attempts = UserChallengeAttempt.objects.filter(
            challenge=challenge, status='completed'
        ).select_related('user').order_by('-points_earned', 'completed_at')[:20] # Top 20

        # Thêm rank
        # queryset_with_rank = UserChallengeAttempt.objects.filter(
        #     challenge=challenge, status='completed'
        # ).annotate(
        #     rank=Window(
        #         expression=Rank(),
        #         order_by=[F('points_earned').desc(), F('completed_at').asc()]
        #     )
        # ).select_related('user')[:20]
        # serializer = ChallengeLeaderboardEntrySerializer(queryset_with_rank, many=True)
        
        # Cách đơn giản hơn để thêm rank vào serializer (nếu không dùng Window function phức tạp)
        ranked_data = []
        for i, attempt in enumerate(leaderboard_attempts):
            serialized_attempt = ChallengeLeaderboardEntrySerializer(attempt).data
            serialized_attempt['rank'] = i + 1
            ranked_data.append(serialized_attempt)
            
        return Response(ranked_data)


class ChallengeExerciseSubmitAttemptView(APIView):
    """
    API endpoint for a user to submit their attempt for a specific ChallengeExercise.
    This will involve speech-to-text, scoring, and updating challenge progress.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request, challenge_pk, exercise_pk):
        user = request.user
        audio_file = request.FILES.get("audio_file")

        if not audio_file:
            return Response({"error": "Missing 'audio_file'."}, status=status.HTTP_400_BAD_REQUEST)

        challenge = get_object_or_404(Challenge, pk=challenge_pk)
        challenge_exercise = get_object_or_404(ChallengeExercise, pk=exercise_pk, challenge=challenge)
        speaking_text_obj = challenge_exercise.speaking_text

        # 0. Kiểm tra user đã start challenge chưa
        try:
            user_challenge_attempt = UserChallengeAttempt.objects.get(user=user, challenge=challenge)
            if user_challenge_attempt.status == 'completed':
                 return Response({"error": "You have already completed this challenge."}, status=status.HTTP_400_BAD_REQUEST)
            if user_challenge_attempt.status == 'not_started': # Nên được xử lý bởi start_challenge endpoint
                 user_challenge_attempt.status = 'in_progress'
                 user_challenge_attempt.save()

        except UserChallengeAttempt.DoesNotExist:
            return Response({"error": "You have not started this challenge yet. Please start the challenge first."}, status=status.HTTP_400_BAD_REQUEST)
        
        # Lấy hoặc tạo UserChallengeExerciseAttempt
        user_exercise_attempt, created = UserChallengeExerciseAttempt.objects.get_or_create(
            user_challenge_attempt=user_challenge_attempt,
            challenge_exercise=challenge_exercise
        )
        if user_exercise_attempt.is_completed:
             return Response({"message": "You have already completed this exercise.", "data": UserChallengeExerciseAttemptSerializer(user_exercise_attempt).data}, status=status.HTTP_200_OK)


        # --- Các bước xử lý audio tương tự SubmitSpeakingAPIView ---
        # 1. Save and Convert Audio (nếu cần)
        temp_dir = os.path.join(settings.MEDIA_ROOT, 'temp_challenge_submissions')
        os.makedirs(temp_dir, exist_ok=True)
        temp_filename = f"{user.id}_ch{challenge_pk}_ex{exercise_pk}_{timezone.now().strftime('%Y%m%d%H%M%S%f')}.webm" # Thêm microsecond để unique hơn
        temp_path = os.path.join(temp_dir, temp_filename)

        try:
            with default_storage.open(temp_path, 'wb+') as destination:
                for chunk in audio_file.chunks():
                    destination.write(chunk)
        except Exception as e:
            # Log lỗi
            return Response({"error": f"Failed to save uploaded audio file: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        wav_path = temp_path.replace('.webm', '.wav')
        try:
            sound = AudioSegment.from_file(temp_path, format="webm")
            sound.export(wav_path, format="wav")
        except Exception as e:
            if os.path.exists(temp_path): os.remove(temp_path)
            return Response({"error": f"Failed to convert audio to WAV: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # 2. Speech Recognition
        recognizer = sr.Recognizer()
        recognized_text_raw = ""
        # (Copy logic nhận dạng từ SubmitSpeakingAPIView, bao gồm chunking nếu cần)
        try:
            with sr.AudioFile(wav_path) as source:
                audio_data = recognizer.record(source)
                recognized_text_raw = recognizer.recognize_google(audio_data, language=speaking_text_obj.language or "en-US") # Sử dụng ngôn ngữ của speaking_text
        except sr.UnknownValueError:
            # Xóa file tạm
            if os.path.exists(temp_path): os.remove(temp_path)
            if os.path.exists(wav_path): os.remove(wav_path)
            return Response({"error": "Could not understand audio or no speech detected."}, status=status.HTTP_400_BAD_REQUEST)
        except sr.RequestError as e:
            if os.path.exists(temp_path): os.remove(temp_path)
            if os.path.exists(wav_path): os.remove(wav_path)
            return Response({"error": f"Speech recognition service error: {e}"}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
        except Exception as e:
             if os.path.exists(temp_path): os.remove(temp_path)
             if os.path.exists(wav_path): os.remove(wav_path)
             return Response({"error": f"An unexpected error during speech recognition: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


        # 3. Get Original Text
        original_text = speaking_text_obj.content # Đã là TextField

        # 4. Calculate Score
        try:
            # Giả sử bạn có hàm này: from .utils.score import calculate_score
            # score_result = calculate_score(recognized_text_raw, original_text)
            # Ví dụ mock:
            import difflib
            similarity = difflib.SequenceMatcher(None, recognized_text_raw.lower(), original_text.lower()).ratio()
            score_value = round(similarity * 100)
            score_result = {"score": score_value, "details": {"recognized": recognized_text_raw, "similarity": similarity, "word_diff": "..."}}

        except Exception as e:
            if os.path.exists(temp_path): os.remove(temp_path)
            if os.path.exists(wav_path): os.remove(wav_path)
            return Response({"error": f"Failed to calculate score: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # 5. Tạo UserPracticeLog
        try:
            practice_log = UserPracticeLog.objects.create(
                user=user,
                speaking_text=speaking_text_obj,
                score=score_result.get('score', 0),
                details=score_result.get('details', {})
                # user_audio_path=wav_path # Có thể lưu đường dẫn file audio đã xử lý
            )
        except Exception as e:
            # Log lỗi, nhưng vẫn có thể tiếp tục nếu việc tạo log không quá quan trọng bằng việc cập nhật challenge
            print(f"Error creating UserPracticeLog for challenge exercise: {str(e)}")
            practice_log = None # Đảm bảo practice_log là None nếu tạo lỗi

        # 6. Cập nhật UserChallengeExerciseAttempt
        user_exercise_attempt.user_practice_log = practice_log
        user_exercise_attempt.is_completed = True
        user_exercise_attempt.score_at_completion = score_result.get('score', 0)
        user_exercise_attempt.completed_at = timezone.now()
        user_exercise_attempt.save()

        # 7. Cập nhật UserChallengeAttempt (status, points)
        progress_info = user_challenge_attempt.update_progress_and_points()

        # 8. Cập nhật UserChallengeStreak (nếu challenge hoàn thành)
        if user_challenge_attempt.status == 'completed':
            user_streak, _ = UserChallengeStreak.objects.get_or_create(user=user)
            user_streak.update_streak(user_challenge_attempt.completed_at.date())
            # TODO: check_and_award_achievements_for_challenge_completion(user, challenge)

        # 9. Dọn dẹp file tạm

            if os.path.exists(temp_path): os.remove(temp_path)
            if os.path.exists(wav_path): os.remove(wav_path)
        
        # 10. Trả kết quả
        return Response({
            "message": "Exercise attempt submitted successfully.",
            "recognized_text": recognized_text_raw,
            "score_result": score_result,
            "exercise_attempt_status": UserChallengeExerciseAttemptSerializer(user_exercise_attempt).data,
            "challenge_attempt_status": UserChallengeAttemptSerializer(user_challenge_attempt, context={'request': request}).data,
            "challenge_progress": progress_info
        }, status=status.HTTP_200_OK)


class UserChallengeDataView(APIView):
    """
    API endpoint to get consolidated challenge-related data for the current user.
    - "Your Challenge Stats": Aggregated stats.
    - "Weekly Achievement": Current best/relevant achievement or streak.
    - List of active challenges with user's progress.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        # 1. Your Challenge Stats
        completed_challenges_count = UserChallengeAttempt.objects.filter(user=user, status='completed').count()
        active_challenges_attempts = UserChallengeAttempt.objects.filter(user=user, status='in_progress')
        active_challenges_count = active_challenges_attempts.count()
        total_points_earned = sum(attempt.points_earned for attempt in UserChallengeAttempt.objects.filter(user=user))
        
        user_streak, _ = UserChallengeStreak.objects.get_or_create(user=user)
        current_streak = user_streak.current_streak_days

        challenge_stats = {
            "challenges_completed": completed_challenges_count,
            "active_challenges": active_challenges_count,
            "points_earned": total_points_earned,
            "current_streak_days": current_streak,
        }

        # 2. Weekly Achievement / User Achievements
        # Lấy achievement nổi bật nhất hoặc gần đây nhất, ví dụ: "Consistency Champion" nếu streak >= 5
        # Đây là ví dụ, bạn cần logic cụ thể hơn để xác định "Weekly Achievement"
        weekly_achievement_data = None
        consistency_achievement = Achievement.objects.filter(name__icontains="Consistency Champion").first() # Giả sử tên achievement
        if consistency_achievement:
            try:
                user_cons_achievement = UserAchievement.objects.get(user=user, achievement=consistency_achievement)
                weekly_achievement_data = UserAchievementSerializer(user_cons_achievement).data
            except UserAchievement.DoesNotExist:
                 # Kiểm tra xem user có đủ điều kiện cho achievement này không (ví dụ streak)
                if current_streak >= consistency_achievement.criteria.get("days", 5): # Giả sử criteria có dạng {"days": 5}
                    # Trao achievement nếu chưa có
                    ua, created = UserAchievement.objects.get_or_create(
                        user=user, achievement=consistency_achievement,
                        defaults={'achieved_at': timezone.now()}
                    )
                    if created and consistency_achievement.points_reward > 0:
                        # TODO: Cộng điểm cho user (nếu achievement có điểm thưởng)
                        pass
                    weekly_achievement_data = UserAchievementSerializer(ua).data
                else: # Nếu không có achievement và không đủ điều kiện
                    weekly_achievement_data = {
                        "name": consistency_achievement.name,
                        "description": consistency_achievement.description,
                        "icon_url": consistency_achievement.icon_url,
                        "message": f"Complete challenges for {consistency_achievement.criteria.get('days', 5)} consecutive days to earn this!",
                        "current_progress_days": current_streak,
                        "target_days": consistency_achievement.criteria.get('days', 5)
                    }


        # Lấy tất cả achievements của user
        all_user_achievements = UserAchievement.objects.filter(user=user).select_related('achievement')
        
        return Response({
            "challenge_stats": challenge_stats,
            "weekly_achievement_highlight": weekly_achievement_data, # Thông tin cho phần "Weekly Achievement" trên UI
            "all_user_achievements": UserAchievementSerializer(all_user_achievements, many=True).data,
        }, status=status.HTTP_200_OK)

# ==============================================================================
#                                 LEADERBOARD API 
# ==============================================================================
from django.db.models import Sum, Q, Count, Case, When, Value, IntegerField
from django.db.models.functions import Coalesce
from datetime import timedelta, date
from .serializers import ( 
    GlobalLeaderboardEntrySerializer, UserSerializer, UserChallengeStreakSerializer, GlobalLeaderboardUserSerializer,
)

class GlobalLeaderboardView(APIView):
    permission_classes = [IsAuthenticated] # Hoặc AllowAny nếu leaderboard công khai

    def _get_date_range(self, period_filter):
        today = timezone.now().date()
        start_date = None
        end_date = today # Mặc định kết thúc là hôm nay

        if period_filter == 'weekly':
            # Tính từ thứ Hai của tuần này đến Chủ Nhật (hoặc đến hôm nay nếu tuần chưa kết thúc)
            start_date = today - timedelta(days=today.weekday())
        elif period_filter == 'monthly':
            start_date = today.replace(day=1)
        # 'all_time' thì start_date sẽ là None (không lọc theo ngày bắt đầu)
        
        return start_date, end_date # end_date luôn là today cho weekly/monthly để tính đến hiện tại

    def _calculate_points_for_users(self, user_ids, start_date, end_date):
        """
        Tính tổng điểm cho danh sách user_ids trong khoảng thời gian cho trước.
        Bao gồm điểm từ UserPracticeLog và UserChallengeAttempt.
        """
        user_points_map = {user_id: 0 for user_id in user_ids}

        # 1. Điểm từ UserPracticeLog
        practice_logs_query = UserPracticeLog.objects.filter(user_id__in=user_ids)
        if start_date:
            # practice_date là DateTimeField, cần so sánh cẩn thận
            # Nếu start_date là đầu ngày, end_date là cuối ngày
            datetime_start = timezone.make_aware(timezone.datetime.combine(start_date, timezone.datetime.min.time())) if start_date else None
            datetime_end = timezone.make_aware(timezone.datetime.combine(end_date, timezone.datetime.max.time())) if end_date else None
            
            if datetime_start:
                practice_logs_query = practice_logs_query.filter(practice_date__gte=datetime_start)
            if datetime_end: # Luôn có end_date cho weekly/monthly
                 practice_logs_query = practice_logs_query.filter(practice_date__lte=datetime_end)

        practice_points = practice_logs_query.values('user_id').annotate(
            total_practice_score=Sum('score')
        ).order_by('user_id')

        for entry in practice_points:
            if entry['user_id'] in user_points_map and entry['total_practice_score'] is not None:
                user_points_map[entry['user_id']] += int(entry['total_practice_score'])

        # 2. Điểm từ UserChallengeAttempt (chỉ tính challenge đã 'completed')
        challenge_attempts_query = UserChallengeAttempt.objects.filter(user_id__in=user_ids, status='completed')
        if start_date: # Lọc theo ngày hoàn thành challenge
            if datetime_start:
                challenge_attempts_query = challenge_attempts_query.filter(completed_at__gte=datetime_start)
            if datetime_end: # Luôn có end_date
                challenge_attempts_query = challenge_attempts_query.filter(completed_at__lte=datetime_end)
        
        challenge_points = challenge_attempts_query.values('user_id').annotate(
            total_challenge_points_earned=Sum('points_earned')
        ).order_by('user_id')

        for entry in challenge_points:
            if entry['user_id'] in user_points_map and entry['total_challenge_points_earned'] is not None:
                user_points_map[entry['user_id']] += entry['total_challenge_points_earned']
        
        return user_points_map


    def get(self, request):
        period_filter = request.query_params.get('period', 'all_time') # 'weekly', 'monthly', 'all_time'
        # language_filter = request.query_params.get('language', None) # Tạm thời chưa dùng

        start_date, end_date = self._get_date_range(period_filter)

        # Lấy tất cả user active (hoặc có hoạt động gần đây để tối ưu)
        # Để đơn giản, ban đầu lấy tất cả users. Cần tối ưu cho hệ thống lớn.
        all_users = User.objects.filter(is_active=True) # Có thể thêm .only('id', 'username', 'first_name', 'last_name')

        # Tính điểm cho tất cả users
        # Lưu ý: Việc này có thể rất chậm với nhiều users. Cần cơ chế caching hoặc pre-computation.
        user_ids = list(all_users.values_list('id', flat=True))
        user_total_points_map = self._calculate_points_for_users(user_ids, start_date, end_date)
        
        leaderboard_data = []
        for user_obj in all_users:
            total_points = user_total_points_map.get(user_obj.id, 0)
            if total_points == 0 and period_filter != 'all_time': # Chỉ hiện user có điểm trong kỳ nếu không phải all_time
                continue

            user_streak, _ = UserChallengeStreak.objects.get_or_create(user=user_obj)
            
            leaderboard_data.append({
                'user_id': user_obj.id, # Giữ user_id để map lại với user_obj
                'user_instance': user_obj, # Giữ instance để serialize
                'total_points': total_points,
                'current_streak_days': user_streak.current_streak_days if user_streak else 0,
            })

        # Sắp xếp leaderboard theo tổng điểm, sau đó theo streak
        leaderboard_data.sort(key=lambda x: (x['total_points'], x['current_streak_days']), reverse=True)

        # Gán rank và serialize
        ranked_leaderboard_entries = []
        current_user_rank = None
        current_user_id = request.user.id if request.user.is_authenticated else None
        
        for i, entry_data in enumerate(leaderboard_data):
            rank = i + 1
            serialized_user = GlobalLeaderboardUserSerializer(entry_data['user_instance']).data
            
            ranked_leaderboard_entries.append({
                'rank': rank,
                'user': serialized_user,
                'total_points': entry_data['total_points'],
                'current_streak_days': entry_data['current_streak_days'],
                # 'trend_percentage': 0 # Mock trend
            })
            if current_user_id and entry_data['user_id'] == current_user_id:
                current_user_rank = rank
        
        # Lấy top N (ví dụ: top 100 cho bảng, top 3 cho card)
        top_3_users = ranked_leaderboard_entries[:3]
        table_rankings = ranked_leaderboard_entries # Hoặc ranked_leaderboard_entries[:100] nếu muốn giới hạn

        # Thông tin "Your Ranking"
        total_learners = all_users.count()
        user_ranking_stats_data = None
        if current_user_id:
            current_user_points = user_total_points_map.get(current_user_id, 0)
            user_streak_obj, _ = UserChallengeStreak.objects.get_or_create(user_id=current_user_id)
            current_user_streak = user_streak_obj.current_streak_days if user_streak_obj else 0
            
            points_to_next = None
            if current_user_rank and current_user_rank > 1:
                user_ahead_points = leaderboard_data[current_user_rank - 2]['total_points'] # -2 vì index từ 0 và rank từ 1
                points_to_next = max(0, user_ahead_points - current_user_points +1)


            user_ranking_stats_data = {
                'current_rank': current_user_rank,
                'total_learners': total_learners,
                'points_to_next_tier': points_to_next, # Cần logic cụ thể cho "next tier"
                'user_total_points': current_user_points,
                'user_current_streak_days': current_user_streak
            }

        return Response({
            "your_ranking_stats": user_ranking_stats_data,
            "top_performers": top_3_users, # Top 3 users
            "leaderboard_rankings": table_rankings, # Danh sách cho bảng
            "filter_options": {"period": period_filter} # Thông tin filter đã áp dụng
        }, status=status.HTTP_200_OK)
    
##################################################### AI #######################################################
from .utils.mistral_api import ask_mistral
from gtts import gTTS
import time
from django.conf import settings

class DialogueAPIView(APIView):
    def post(self, request):
        audio_file = request.FILES.get("audio_file")
        print("[✔] Nhận file:", audio_file.name, audio_file.size)

        if not audio_file:
            return Response({"error": "Missing audio file."}, status=400)

        # [1] Lưu file tạm
        temp_path = default_storage.save('temp_input.webm', audio_file)
        full_path = os.path.join(default_storage.location, temp_path)

        # [2] Chuyển sang WAV
        wav_path = full_path.replace('.webm', '.wav')
        sound = AudioSegment.from_file(full_path, format="webm")
        sound.export(wav_path, format="wav")

        # [3] Nhận dạng giọng nói
        recognizer = sr.Recognizer()
        with sr.AudioFile(wav_path) as source:
            audio_data = recognizer.record(source)
            try:
                user_text = recognizer.recognize_google(audio_data, language="en-US")
                print("[✔] Văn bản nhận được:", user_text)
            except sr.UnknownValueError:
                return Response({"error": "Không thể nhận diện giọng nói"}, status=400)
            except sr.RequestError:
                return Response({"error": "Lỗi kết nối Google Speech API"}, status=500)


        # [4] Gửi văn bản lên Mistral AI
        ai_text = ask_mistral(user_text)

        # [5] TTS: chuyển text thành audio
        tts = gTTS(ai_text)

        # Tạo thư mục con ai_responses trong MEDIA_ROOT
        output_dir = os.path.join(settings.MEDIA_ROOT, "ai_responses")
        os.makedirs(output_dir, exist_ok=True)

        # Đặt tên file theo timestamp để tránh bị ghi đè
        filename = f"response_{int(time.time())}.mp3"
        output_path = os.path.join(output_dir, filename)

        # Lưu file đúng chỗ
        tts.save(output_path)

        # Tạo URL trả về
        audio_url = request.build_absolute_uri(f"/media/ai_responses/{filename}")

        # [6] Trả kết quả
        return Response({
            "user_text": user_text,
            "ai_text": ai_text,
            "ai_audio_url": request.build_absolute_uri(f"/media/ai_responses/{filename}")
        }, status=200)
