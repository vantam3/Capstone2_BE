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
User = get_user_model() # Ensure User is the correct model

class DashboardStatsView(APIView):
    """
    API endpoint to retrieve statistics for the admin dashboard, using data from
    `auth_user` and `app_userpracticelog` (adjust app name if needed).
    Requires admin privileges.
    """
    permission_classes = [IsAdminUser]

    def get(self, request, format=None):
        # 1. Total Users: Count all users in `auth_user` table
        total_users = User.objects.count()

        # 2. Active Users: Count users in `auth_user` where `is_active` is True
        active_users = User.objects.filter(is_active=True).count()

        # 3. Recent Activity Users:
        # Count distinct user_ids from `app_userpracticelog`
        # with `practice_date` within the last 7 days.
        recent_days = 7
        cutoff_date = timezone.now() - timedelta(days=recent_days)

        # Assumes the model name is UserPracticeLog and the app label is implicitly found
        # If your app name is different, specify like: `yourapp.UserPracticeLog`
        recent_activity_users = UserPracticeLog.objects.filter(
            practice_date__gte=cutoff_date
        ).values('user').distinct().count() # Use the foreign key 'user' which links to auth_user

        # Data to return to the frontend
        data = {
            'total_users': total_users,
            'active_users': active_users,
            'recent_activity_users': recent_activity_users,
            'recent_activity_days': recent_days
        }

        return Response(data, status=status.HTTP_200_OK)


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
    queryset = Level.objects.all().order_by('id') # Get all levels, ordered by ID
    serializer_class = LevelSerializer
    # No specific permissions needed usually, assuming levels are public info
    # permission_classes = [IsAuthenticated] # Or require login if levels are not public