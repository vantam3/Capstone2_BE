from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import FileResponse  # Thêm import FileResponse từ django.http
import os
from rest_framework import status
from .models import Genre, SpeakingText, Audio, Level, SpeakingResult, UserAudio
from .serializers import GenreSerializer, SpeakingTextSerializer, AudioSerializer,UserSerializer, SpeakingResult, LevelSerializer, UserAudioSerializer
from django.http import HttpResponse
from django.contrib.auth.models import User
import speech_recognition as sr
from pydub import AudioSegment
import base64
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from .utils.score import calculate_score  # bạn đã có hàm này
from django.core.files.storage import default_storage

from rest_framework import generics
def home(request):
    return HttpResponse("SPEAKING PRO API")
# ==============================================================================
# API authentication
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate, get_user_model
from django.core.mail import send_mail
from datetime import date, timedelta
from .models import UserLoginStreak
from rest_framework import generics, permissions
from .serializers import ResetPasswordSerializer
from django.core.cache import cache
import random
import string

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

        auth_user = authenticate(request, username=username, password=password)

        if auth_user is not None:
            # Người dùng xác thực thành công
            today = date.today()
            streak_record, created = UserLoginStreak.objects.get_or_create(user=auth_user)

            if created or streak_record.last_login_date is None:
                streak_record.streak_count = 1
            elif streak_record.last_login_date == today:
                pass # Đã đăng nhập hôm nay
            elif streak_record.last_login_date == (today - timedelta(days=1)):
                streak_record.streak_count += 1
            else:
                streak_record.streak_count = 1
            
            # Chỉ cập nhật last_login_date nếu nó chưa phải là hôm nay
            # (hoặc khi streak được set/reset)
            if streak_record.last_login_date != today or created:
                 streak_record.last_login_date = today
            
            streak_record.save()

            refresh = RefreshToken.for_user(auth_user)
            user_data = {
                'id': auth_user.id,
                'username': auth_user.username,
                'first_name': auth_user.first_name,
                'last_name': auth_user.last_name,
                'email': auth_user.email,
                'is_superuser': auth_user.is_superuser,
            }
            return Response({
                'token': str(refresh.access_token),
                'user': user_data
            }, status=status.HTTP_200_OK)
        else:
            # Xác thực thất bại
            try:
                User.objects.get(username=username)
                # User tồn tại, vậy là sai mật khẩu
                return Response({'message': 'Invalid password!'},
                                status=status.HTTP_401_UNAUTHORIZED)
            except User.DoesNotExist:
                # User không tồn tại
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

class UserProfileUpdateAPIView(generics.UpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user

    def perform_update(self, serializer):
        serializer.save()

# ==========================================================================================================================================
# api search
from rest_framework import generics
from django.db.models import Q
from .models import SpeakingText
from .serializers import SpeakingTextSerializer

class SpeakingTextSearchAPIView(generics.ListAPIView):
    serializer_class = SpeakingTextSerializer

    def get_queryset(self):
        queryset = SpeakingText.objects.all()
        genre_id = self.request.query_params.get('genre', None)
        title = self.request.query_params.get('title', None)

        if genre_id:
            queryset = queryset.filter(genre_id=genre_id)

        if title:
            queryset = queryset.filter(title__icontains=title)

        return queryset
# ==========================================================================================================================================
# API Challenge
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Challenge, ChallengeExercise, UserChallengeProgress, UserExerciseAttempt
from .serializers import ChallengeSerializer, UserChallengeProgressSerializer, ChallengeExerciseDetailSerializer
from .utils.score import calculate_score
from pydub import AudioSegment
import speech_recognition as sr
import os
from django.utils import timezone
from django.core.files.storage import default_storage
class ChallengeListAPIView(APIView):
    def get(self, request):
        challenges = Challenge.objects.all()
        serializer = ChallengeSerializer(challenges, many=True)
        return Response(serializer.data)

class ChallengeDetailAPIView(APIView):
    def get(self, request, challenge_pk):
        try:
            challenge = Challenge.objects.get(pk=challenge_pk)
        except Challenge.DoesNotExist:
            return Response({"error": "Challenge not found"}, status=404)
        serializer = ChallengeSerializer(challenge)
        return Response(serializer.data)

class ChallengeExerciseDetailAPIView(generics.RetrieveAPIView):
    queryset = ChallengeExercise.objects.all()
    serializer_class = ChallengeExerciseDetailSerializer
    permission_classes = [permissions.AllowAny] 

class StartChallengeAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, challenge_pk):
        user = request.user
        challenge = Challenge.objects.get(pk=challenge_pk)
        progress, _ = UserChallengeProgress.objects.get_or_create(user=user, challenge=challenge)
        if progress.status == 'not_started':
            progress.status = 'in_progress'
            progress.save()
        return Response({"message": "Challenge started", "status": progress.status})

class ChallengeExerciseDetailAPIView(generics.RetrieveAPIView):
    queryset = ChallengeExercise.objects.all()
    serializer_class = ChallengeExerciseDetailSerializer
    permission_classes = [permissions.AllowAny]

class SubmitExerciseAttemptAPIView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser]

    def update_user_weekly_score(self, user, score):
        today = timezone.now().date()
        year, week, _ = today.isocalendar()
        obj, created = UserWeeklyScore.objects.get_or_create(user=user, year=year, week=week)
        obj.total_score += score
        obj.save()

    def update_user_streak(self, user):
        today = timezone.now().date()
        streak, created = UserLoginStreak.objects.get_or_create(user=user)

        if streak.last_login_date is None:
            streak.streak_count = 1
        else:
            delta = (today - streak.last_login_date).days
            if delta == 1:
                streak.streak_count += 1
            elif delta > 1:
                streak.streak_count = 1  # reset nếu gián đoạn

        streak.last_login_date = today
        streak.save()

    def post(self, request, exercise_pk):
        user = request.user
        audio_file = request.FILES.get('audio_file')
        if not audio_file:
            return Response({"error": "Missing audio file"}, status=400)

        try:
            exercise = ChallengeExercise.objects.get(pk=exercise_pk)
        except ChallengeExercise.DoesNotExist:
            return Response({"error": "Exercise not found"}, status=404)

        # [1] Chuyển đổi WebM -> WAV
        temp_path = default_storage.save('temp_challenge_input.webm', audio_file)
        full_path = os.path.join(default_storage.location, temp_path)
        wav_path = full_path.replace('.webm', '.wav')
        sound = AudioSegment.from_file(full_path, format="webm")
        sound.export(wav_path, format="wav")

        # [2] Nhận diện giọng nói
        recognizer = sr.Recognizer()
        with sr.AudioFile(wav_path) as source:
            audio_data = recognizer.record(source)
            try:
                transcribed_text = recognizer.recognize_google(audio_data, language="en-US")
            except Exception:
                return Response({"error": "Speech recognition failed"}, status=500)

        # [3] Giải mã content gốc
        try:
            original_bytes = bytes.fromhex(exercise.speaking_text_content.decode("utf-8"))
            original_text = original_bytes.decode("utf-8")
        except Exception:
            return Response({"error": "Failed to decode original text"}, status=500)

        # Tính điểm
        result = calculate_score(transcribed_text, original_text)

        # [4] Lưu tiến trình
        challenge = exercise.challenge
        progress, _ = UserChallengeProgress.objects.get_or_create(user=user, challenge=challenge)
        UserExerciseAttempt.objects.create(
            user_challenge_progress=progress,
            challenge_exercise=exercise,
            user_audio_file_path=audio_file,
            transcribed_text=transcribed_text,
            score=result['score'],
            detailed_feedback=result
        )

        progress.score += result['score']
        total = challenge.exercises.count()
        done = UserExerciseAttempt.objects.filter(user_challenge_progress=progress).values('challenge_exercise').distinct().count()
        progress.completion_percentage = round(100 * done / total, 2)
        if progress.completion_percentage == 100:
            progress.status = 'completed'
            progress.completed_date = timezone.now()
        progress.save()

        # [5] Cập nhật bảng điểm tuần và chuỗi đăng nhập
        self.update_user_weekly_score(user, result['score'])
        self.update_user_streak(user)

        # Dọn dẹp file tạm
        os.remove(full_path)
        os.remove(wav_path)

        return Response(result, status=200)

class MyChallengeProgressAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        progresses = UserChallengeProgress.objects.filter(user=request.user)
        serializer = UserChallengeProgressSerializer(progresses, many=True)
        return Response(serializer.data)
# ==========================================================================================================================================
# API leaderboard
from .models import UserWeeklyScore, UserExerciseAttempt, UserLoginStreak
from django.db.models import Sum
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Max, F, Sum
from django.contrib.auth.models import User
from datetime import timedelta
from django.utils import timezone
from collections import defaultdict

class ChallengeLeaderboardAPIView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request, challenge_id):
        try:
            challenge = Challenge.objects.get(id=challenge_id)
        except Challenge.DoesNotExist:
            return Response({"error": "Challenge not found."}, status=404)

        # Lấy danh sách exercise thuộc challenge này
        exercises = ChallengeExercise.objects.filter(challenge=challenge)

        # Lấy tất cả các attempt liên quan
        attempts = UserExerciseAttempt.objects.filter(challenge_exercise__in=exercises)

        # Tạo dict {(user_id, exercise_id): max_score}
        from collections import defaultdict
        user_scores = defaultdict(lambda: defaultdict(float))

        for attempt in attempts:
            user_id = attempt.user_challenge_progress.user.id
            exercise_id = attempt.challenge_exercise.id
            current_score = float(attempt.score)

            if user_scores[user_id][exercise_id] < current_score:
                user_scores[user_id][exercise_id] = current_score

        # Tính tổng điểm mỗi user
        leaderboard = []
        for user_id, exercise_scores in user_scores.items():
            total = sum(exercise_scores.values())
            try:
                user = User.objects.get(id=user_id)
                leaderboard.append({
                    "user_id": user.id,
                    "username": user.username,
                    "score": round(total)
                })
            except User.DoesNotExist:
                continue

        # Sắp xếp giảm dần theo điểm
        leaderboard = sorted(leaderboard, key=lambda x: x['score'], reverse=True)

        return Response({"challenge_id": challenge_id, "leaderboard": leaderboard})

class GlobalLeaderboardAPIView(APIView):
    def get(self, request):
        now = timezone.now()
        one_week_ago = now - timedelta(days=7)

        # Tính điểm cao nhất mỗi bài / người dùng
        attempts = UserExerciseAttempt.objects.all()
        current_scores = defaultdict(lambda: defaultdict(float))
        weekly_scores = defaultdict(float)

        for attempt in attempts:
            uid = attempt.user_challenge_progress.user.id
            eid = attempt.challenge_exercise.id
            score = float(attempt.score)
            ts = attempt.attempted_at

            if current_scores[uid][eid] < score:
                current_scores[uid][eid] = score
            if ts >= one_week_ago:
                if weekly_scores[uid] < score:
                    weekly_scores[uid] += score

        # Tổng điểm theo người dùng
        leaderboard = []
        for uid, exercise_scores in current_scores.items():
            try:
                user = User.objects.get(id=uid)
                total_score = sum(exercise_scores.values())
                streak_data = UserLoginStreak.objects.filter(user=user).aggregate(max_streak=Max("streak_count")) or {}
                max_streak = streak_data.get("max_streak") or 0

                weekly_total = weekly_scores.get(uid, 0.0)
                last_week_total = total_score - weekly_total
                growth_percent = ((weekly_total / last_week_total) * 100) if last_week_total > 0 else 0

                leaderboard.append({
                    "user_id": uid,
                    "username": user.username,
                    "total_points": round(total_score),
                    "longest_streak": max_streak,
                    "trend": f"{round(growth_percent)}%"
                })
            except User.DoesNotExist:
                continue

        leaderboard = sorted(leaderboard, key=lambda x: x["total_points"], reverse=True)

        return Response({"leaderboard": leaderboard})
# ==========================================================================================================================================
# API Admin summary
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.db.models import Count
from django.utils import timezone
from datetime import timedelta
from collections import defaultdict

from .models import (
    SpeakingText,
    ChallengeExercise,
    UserAudio,
    UserExerciseAttempt,
    UserLoginStreak  # hoặc bảng logins khác nếu có
)

class AdminDashboardSummaryAPIView(APIView):
    def get(self, request):
        now = timezone.now()
        last_week = now - timedelta(days=7)

        # Tổng người dùng & tăng trưởng
        total_users = User.objects.count()
        last_week_users = User.objects.filter(date_joined__gte=last_week).count()
        user_growth_percent = (last_week_users / (total_users - last_week_users + 1e-6)) * 100

        # Tổng số bài nói
        total_speaking_contents = ChallengeExercise.objects.count()
        recent_speaking = ChallengeExercise.objects.filter(created_at__gte=last_week).count()
        content_growth_percent = (recent_speaking / (total_speaking_contents - recent_speaking + 1e-6)) * 100

        # Tổng số lượt luyện tập
        total_attempts = UserAudio.objects.count() + UserExerciseAttempt.objects.count()
        recent_attempts = UserAudio.objects.filter(uploaded_at__gte=last_week).count() + \
                          UserExerciseAttempt.objects.filter(attempted_at__gte=last_week).count()
        attempt_growth_percent = (recent_attempts / (total_attempts - recent_attempts + 1e-6)) * 100

        # Thống kê đăng nhập mỗi ngày trong tuần
        login_data = UserLoginStreak.objects.filter(last_login_date__gte=now - timedelta(days=6))
        daily_login_chart = defaultdict(int)
        for item in login_data:
            weekday = item.last_login_date.strftime('%a')  # Mon, Tue,...
            daily_login_chart[weekday] += 1

        day_order = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
        login_chart_data = [{"day": d, "users": daily_login_chart.get(d, 0)} for d in day_order]

        # Most practiced content
        practice_count = UserExerciseAttempt.objects.values("challenge_exercise__title").annotate(
        count=Count("id")).order_by("-count")[:5]

        most_practiced = [
            {"name": item["challenge_exercise__title"], "count": item["count"]}
            for item in practice_count
        ]
        most_practiced = sorted(most_practiced, key=lambda x: x["count"], reverse=True)[:5]

        return Response({
            "total_users": total_users,
            "user_growth_percent": round(user_growth_percent),
            "total_speaking_contents": total_speaking_contents,
            "content_growth_percent": round(content_growth_percent),
            "total_practice_attempts": total_attempts,
            "attempt_growth_percent": round(attempt_growth_percent),
            "daily_login_chart": login_chart_data,
            "most_practiced_content": most_practiced
        })
# ==========================================================================================================================================
# API Report
from django.utils import timezone
from datetime import timedelta, datetime
from django.db.models import Count, Avg
from django.db.models.functions import TruncDay, TruncWeek, TruncMonth
from collections import defaultdict

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from .models import (
    SpeakingText,
    ChallengeExercise,
    UserExerciseAttempt,
    UserLoginStreak,
    Genre,
    SpeakingResult,
    UserChallengeProgress
)

class AdminReportsDataAPIView(APIView):

    def _get_date_range(self, period_str):
        now = timezone.now()
        end_date = now.replace(hour=23, minute=59, second=59, microsecond=999999) # Cuối ngày hiện tại
        
        if period_str == 'day': # Today
            start_date = now.replace(hour=0, minute=0, second=0, microsecond=0)
        elif period_str == 'week': # This Week (tính từ Thứ Hai của tuần hiện tại)
            start_date = (now - timedelta(days=now.weekday())).replace(hour=0, minute=0, second=0, microsecond=0)
        elif period_str == 'month': # This Month
            start_date = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        else: # Mặc định là 'This Week' nếu period_str không hợp lệ
            start_date = (now - timedelta(days=now.weekday())).replace(hour=0, minute=0, second=0, microsecond=0)
            period_str = 'week' # Cập nhật lại period_str để response được chính xác
        
        return start_date, end_date, period_str

    def _get_time_unit_accessor(self, granularity_str):
        # Mặc định là 'day' nếu granularity_str không hợp lệ hoặc không được cung cấp
        if granularity_str == 'month':
            return TruncMonth, "%Y-%m"
        elif granularity_str == 'week':
            # TruncWeek trả về Thứ Hai của tuần. %W (00-53, Thứ Hai là ngày đầu tuần)
            return TruncWeek, "%Y-W%W" 
        return TruncDay, "%Y-%m-%d" # Mặc định là 'day'

    def get_user_activity_preview_data(self, start_date, end_date, trunc_func, date_format_str):
        # Logins
        logins_q = (UserLoginStreak.objects
                    .filter(last_login_date__range=(start_date.date(), end_date.date()))
                    .annotate(period_unit=trunc_func('last_login_date'))
                    .values('period_unit')
                    .annotate(count=Count('user', distinct=True))
                    .order_by('period_unit'))
        
        # Exercises Completed
        completed_q = (UserChallengeProgress.objects
                       .filter(status='completed', completed_date__range=(start_date, end_date))
                       .annotate(period_unit=trunc_func('completed_date'))
                       .values('period_unit')
                       .annotate(count=Count('id'))
                       .order_by('period_unit'))

        # Practice Attempts
        challenge_attempts_q = (UserExerciseAttempt.objects
                                .filter(attempted_at__range=(start_date, end_date))
                                .annotate(period_unit=trunc_func('attempted_at'))
                                .values('period_unit')
                                .annotate(count=Count('id'))
                                .order_by('period_unit'))
        
        general_practice_q = (SpeakingResult.objects
                              .filter(timestamp__range=(start_date, end_date))
                              .annotate(period_unit=trunc_func('timestamp'))
                              .values('period_unit')
                              .annotate(count=Count('id'))
                              .order_by('period_unit'))

        # Gộp dữ liệu: Tạo một tập hợp tất cả các 'period_unit' từ các query
        all_periods = set()
        for q_set in [logins_q, completed_q, challenge_attempts_q, general_practice_q]:
            for item in q_set:
                all_periods.add(item['period_unit'])
        
        sorted_periods = sorted(list(all_periods))
        
        results = []
        for period_dt_obj in sorted_periods:
            period_key_str = period_dt_obj.strftime(date_format_str)
            
            logins_count = next((item['count'] for item in logins_q if item['period_unit'] == period_dt_obj), 0)
            completed_count = next((item['count'] for item in completed_q if item['period_unit'] == period_dt_obj), 0)
            challenge_attempt_count = next((item['count'] for item in challenge_attempts_q if item['period_unit'] == period_dt_obj), 0)
            general_practice_count = next((item['count'] for item in general_practice_q if item['period_unit'] == period_dt_obj), 0)
            total_attempts = challenge_attempt_count + general_practice_count

            results.append({
                "name": period_key_str,
                "logins": logins_count,
                "exercisesCompleted": completed_count,
                "practiceAttempts": total_attempts 
            })
        return results

    def get_content_engagement_preview_data(self, start_date, end_date):
        genres = Genre.objects.all()
        results = []
        for genre in genres:
            speaking_texts_in_genre = SpeakingText.objects.filter(genre=genre)
            attempts_count = SpeakingResult.objects.filter(
                speaking_text__in=speaking_texts_in_genre,
                timestamp__range=(start_date, end_date)
            ).count()
            
            avg_score_data = SpeakingResult.objects.filter(
                speaking_text__in=speaking_texts_in_genre,
                timestamp__range=(start_date, end_date)
            ).aggregate(avg=Avg('score'))
            average_score = round(avg_score_data['avg'], 1) if avg_score_data['avg'] else 0
            
            if attempts_count > 0 or average_score > 0: 
                results.append({
                    "name": genre.name,
                    "attempts": attempts_count,
                    "averageScore": average_score
                })
        return results

    def get_user_growth_preview_data(self, start_date, end_date, trunc_func, date_format_str):
        user_growth = (User.objects
                       .filter(date_joined__range=(start_date, end_date))
                       .annotate(period_unit=trunc_func('date_joined'))
                       .values('period_unit')
                       .annotate(new_users=Count('id'))
                       .order_by('period_unit'))
        
        results = [{"name": item['period_unit'].strftime(date_format_str), "users": item['new_users']} for item in user_growth]
        return results
        

    def get_learning_performance_preview_data(self, start_date, end_date, trunc_func, date_format_str):
        # Tính điểm trung bình từ UserExerciseAttempt và SpeakingResult gộp lại
        
        all_scores_data = []
        challenge_scores = UserExerciseAttempt.objects.filter(attempted_at__range=(start_date, end_date)).values_list('attempted_at', 'score')
        general_scores = SpeakingResult.objects.filter(timestamp__range=(start_date, end_date)).values_list('timestamp', 'score')

        for timestamp, score in challenge_scores:
            all_scores_data.append({'timestamp': timestamp, 'score': float(score)}) # score của UserExerciseAttempt là FloatField
        for timestamp, score in general_scores:
            all_scores_data.append({'timestamp': timestamp, 'score': float(score)}) # score của SpeakingResult là DecimalField

        # Nhóm theo period_unit và tính trung bình
        grouped_scores = defaultdict(lambda: {'total_score': 0.0, 'count': 0})
        for record in all_scores_data:
            period_key = trunc_func(record['timestamp']).strftime(date_format_str)
            grouped_scores[period_key]['total_score'] += record['score']
            grouped_scores[period_key]['count'] += 1
        
        results = []
        sorted_grouped_scores = sorted(grouped_scores.items(), key=lambda x: x[0]) # Sắp xếp theo chuỗi thời gian
        for period_str_key, data in sorted_grouped_scores:
            avg_score = round(data['total_score'] / data['count'], 1) if data['count'] > 0 else 0
            results.append({
                "name": period_str_key,
                "score": avg_score
            })
        return results

    def get_system_usage_preview_data(self, start_date, end_date):
        return {
            "message": "Dữ liệu sử dụng hệ thống chi tiết (tải server, thời gian phản hồi API, tỷ lệ lỗi) hiện không được theo dõi trong phạm vi các model ứng dụng. Để có báo cáo này, cần các công cụ giám sát và logging chuyên dụng."
        }

    def get(self, request, *args, **kwargs):
        report_type_param = request.query_params.get('reportType', 'userActivity')
        time_range_param = request.query_params.get('timeRange', 'week') # Giá trị từ Select của FE
        # 'Data Grouping' từ FE sẽ quyết định granularity
        granularity_param = request.query_params.get('granularity', 'day') 

        start_date, end_date, actual_time_range_param = self._get_date_range(time_range_param)
        trunc_func, date_format_str = self._get_time_unit_accessor(granularity_param)
        
        preview_data = {}
        if report_type_param == 'userActivity':
            preview_data = self.get_user_activity_preview_data(start_date, end_date, trunc_func, date_format_str)
        elif report_type_param == 'contentEngagement':
            preview_data = self.get_content_engagement_preview_data(start_date, end_date)
        elif report_type_param == 'userGrowth':
            preview_data = self.get_user_growth_preview_data(start_date, end_date, trunc_func, date_format_str)
        elif report_type_param == 'performance':
            preview_data = self.get_learning_performance_preview_data(start_date, end_date, trunc_func, date_format_str)
        elif report_type_param == 'systemUsage':
            preview_data = self.get_system_usage_preview_data(start_date, end_date)
        else:
            return Response({"error": f"Loại báo cáo '{report_type_param}' không được hỗ trợ."}, status=status.HTTP_400_BAD_REQUEST)
            
        return Response({
            "report_type": report_type_param,
            "time_range_requested": time_range_param, # Giá trị FE gửi lên
            "granularity_requested": granularity_param,
            "data_period_applied": { # Khoảng thời gian thực tế được áp dụng
                "start": start_date.strftime('%Y-%m-%d'),
                "end": end_date.strftime('%Y-%m-%d'),
                "type": actual_time_range_param # Loại khoảng thời gian thực tế sau khi xử lý
            },
            "preview_data": preview_data
        }, status=status.HTTP_200_OK)
#     
# ==========================================================================================================================================
# API để lấy danh sách tất cả thể loại
class GenreListView(APIView):
    def get(self, request):
        genres = Genre.objects.all()
        serializer = GenreSerializer(genres, many=True)
        return Response(serializer.data)
#api lay sach theo level va genre
class SpeakingTextFilterAPIView(generics.ListAPIView):
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
            # Lấy đối tượng Audio từ cơ sở dữ liệu theo pk
            audio = Audio.objects.get(pk=pk)
        except Audio.DoesNotExist:
            return Response({"error": "Audio file not found."}, status=status.HTTP_404_NOT_FOUND)

        # Đảm bảo rằng tệp âm thanh tồn tại
        if not audio.audio_file:
            return Response({"error": "Audio file not found."}, status=status.HTTP_404_NOT_FOUND)

        # Trả về URL của tệp âm thanh (FileField sẽ tự động trả về URL)
        audio_url = audio.audio_file.url  # Lấy URL của tệp âm thanh
        full_audio_url = f"http://127.0.0.1:8000{audio_url}"  # Kết hợp domain và đường dẫn
        return Response({"audio_url": full_audio_url}, status=status.HTTP_200_OK)
    
#@api_view(['POST'])
from django.contrib.auth.models import User
from .utils.audio_converter import convert_webm_to_mp3

@csrf_exempt
@api_view(['POST'])
def upload_user_audio(request):
    audio_file = request.FILES.get('audio')

    if audio_file:
        try:
            test_user = User.objects.get(username='tranv')
        except User.DoesNotExist:
            return Response({"error": "Test user does not exist."}, status=status.HTTP_400_BAD_REQUEST)

        # Lưu bản gốc .webm
        user_audio = UserAudio.objects.create(user=test_user, audio_file=audio_file)
        serializer = UserAudioSerializer(user_audio)

        # Đường dẫn file gốc
        input_path = user_audio.audio_file.path

        # Đường dẫn file .mp3 sau khi chuyển đổi
        filename_wo_ext = os.path.splitext(os.path.basename(input_path))[0]
        output_dir = os.path.join(os.path.dirname(input_path), '../../converted_audio/')
        os.makedirs(output_dir, exist_ok=True)
        output_path = os.path.abspath(os.path.join(output_dir, f"{filename_wo_ext}.mp3"))

        # Chuyển đổi WebM -> MP3
        success = convert_webm_to_mp3(input_path, output_path)
        if not success:
            return Response({"error": "Failed to convert audio."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # Xây dựng URL tuyệt đối cho file .mp3
        mp3_relative_url = f"/media/converted_audio/{filename_wo_ext}.mp3"
        mp3_absolute_url = request.build_absolute_uri(mp3_relative_url)

        return Response({
            'original_audio': serializer.data['audio_file'],
            'converted_audio': mp3_absolute_url
        }, status=status.HTTP_201_CREATED)

    return Response({"error": "No audio file provided"}, status=status.HTTP_400_BAD_REQUEST)
def split_audio_to_chunks(audio_path, chunk_length_ms=15000):
    from pydub import AudioSegment
    audio = AudioSegment.from_wav(audio_path)
    chunks = [audio[i:i + chunk_length_ms] for i in range(0, len(audio), chunk_length_ms)]
    return chunks

class SubmitSpeakingAPIView(APIView):
    def post(self, request):
        audio_file = request.FILES.get("audio_file")
        speaking_text_id = request.data.get("speaking_text_id")

        if not audio_file or not speaking_text_id:
            return Response({"error": "Thiếu dữ liệu"}, status=status.HTTP_400_BAD_REQUEST)

        # Lưu file tạm
        temp_path = default_storage.save('temp_input.webm', audio_file)
        full_path = os.path.join(default_storage.location, temp_path)

        # Chuyển webm -> wav để nhận diện giọng nói
        wav_path = full_path.replace('.webm', '.wav')
        sound = AudioSegment.from_file(full_path, format="webm")
        sound.export(wav_path, format="wav")

        # Nhận diện văn bản từ wav
        recognizer = sr.Recognizer()
        try:
            recognizer = sr.Recognizer()
            full_text = ""

            chunks = split_audio_to_chunks(wav_path, chunk_length_ms=15000)

            for i, chunk in enumerate(chunks):
                chunk_path = f"chunk_part_{i}.wav"
                chunk.export(chunk_path, format="wav")

                with sr.AudioFile(chunk_path) as source:
                    audio_data = recognizer.record(source)
                    try:
                        text = recognizer.recognize_google(audio_data, language="en-US")
                        full_text += " " + text
                    except sr.UnknownValueError:
                        print(f"[⚠️] Chunk {i}: không thể nhận diện.")
                    except sr.RequestError:
                        print(f"[❌] Chunk {i}: lỗi kết nối Google API.")

                os.remove(chunk_path)

            user_text_raw = full_text.strip()


        except sr.UnknownValueError:
            return Response({"error": "Không thể nhận diện giọng nói"}, status=status.HTTP_400_BAD_REQUEST)
        except sr.RequestError:
            return Response({"error": "Lỗi dịch vụ nhận diện giọng nói"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # Lấy đoạn văn mẫu gốc
        try:
            speaking_text = SpeakingText.objects.get(id=speaking_text_id)
        except SpeakingText.DoesNotExist:
            return Response({"error": "Văn bản mẫu không tồn tại"}, status=status.HTTP_404_NOT_FOUND)

        # Giải mã nội dung gốc
        try:
            original_bytes = bytes.fromhex(speaking_text.content.decode("utf-8"))
            original_text = original_bytes.decode("utf-8")
        except Exception as e:
            return Response({"error": "Không thể giải mã nội dung đoạn văn mẫu."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # Tính điểm và phân tích chi tiết từng từ
        result = calculate_score(user_text_raw, original_text)

        # Lưu kết quả thô vào DB nếu muốn (tùy bạn)
        SpeakingResult.objects.create(
            speaking_text=speaking_text,
            user_text=user_text_raw,
            score=result["score"]
        )

        # Dọn dẹp file tạm
        os.remove(full_path)
        os.remove(wav_path)

        # Trả kết quả
        return Response(result, status=status.HTTP_200_OK)



class UserListView(APIView):
    def get(self, request):
        users = User.objects.all()  # Lấy tất cả người dùng
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)
from rest_framework.generics import RetrieveAPIView
from django.contrib.auth import get_user_model
from .serializers import UserSerializer

User = get_user_model()

class UserDetailAPIView(RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'id'

#record


        
##################################################### CRUD TAI LIEU #######################################################
# API để thêm một SpeakingText mới
class SpeakingTextCreateAPIView(APIView):
    def post(self, request):
        genre_data = request.data.get('genre')  # Lấy dữ liệu genre từ request
        level_data = request.data.get('level')  # Lấy dữ liệu level từ request

        # Kiểm tra nếu genre là ID hoặc name
        if isinstance(genre_data, dict):  # Nếu genre được gửi dưới dạng dict (chứa name)
            genre_name = genre_data.get('name')  # Lấy name của genre từ request
            genre = Genre.objects.filter(name=genre_name).first()
            if not genre:
                genre = Genre.objects.create(name=genre_name)  # Tạo mới nếu không có
        else:  # Nếu genre là ID
            genre_id = genre_data  # Lấy genre_id trực tiếp từ request
            genre = Genre.objects.filter(id=genre_id).first()
            if not genre:
                return Response({"error": "Genre not found with the provided ID."}, status=status.HTTP_404_NOT_FOUND)

        # Kiểm tra nếu level là ID và lấy level tương ứng
        if isinstance(level_data, dict):  # Nếu level được gửi dưới dạng dict (chứa name)
            level_name = level_data.get('name')  # Lấy name của level từ request
            level = Level.objects.filter(name=level_name).first()
            if not level:
                level = Level.objects.create(name=level_name)  # Tạo mới nếu không có
        else:  # Nếu level là ID
            level_id = level_data  # Lấy level_id trực tiếp từ request
            level = Level.objects.filter(id=level_id).first()
            if not level:
                return Response({"error": "Level not found with the provided ID."}, status=status.HTTP_404_NOT_FOUND)

        # Giải mã nội dung content nếu có
        content_base64 = request.data.get('content')
        if content_base64:
            content_binary = base64.b64decode(content_base64)  # Giải mã base64 thành binary
        else:
            content_binary = None

        # Tạo SpeakingText và lưu vào cơ sở dữ liệu
        serializer = SpeakingTextSerializer(data=request.data)
        if serializer.is_valid():
            # Liên kết với genre và level, lưu content đã giải mã vào cơ sở dữ liệu
            serializer.save(genre=genre, level=level, content=content_binary)  # Lưu vào cơ sở dữ liệu
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#API EDIT
class SpeakingTextUpdateAPIView(generics.UpdateAPIView):
    queryset = SpeakingText.objects.all()  # Lấy tất cả tài liệu
    serializer_class = SpeakingTextSerializer  # Sử dụng SpeakingTextSerializer để cập nhật
    lookup_field = 'id'  # Để tìm tài liệu theo ID
    
#API DELETE
class SpeakingTextDeleteAPIView(generics.DestroyAPIView):
    queryset = SpeakingText.objects.all()  # Lấy tất cả tài liệu
    serializer_class = SpeakingTextSerializer  # Dùng serializer của SpeakingText
    lookup_field = 'id'  # Tìm tài liệu theo ID
    
    
##################################################### CRUD USER #######################################################
class UserCreateAPIView(generics.CreateAPIView):
    queryset = User.objects.all()  # Tất cả người dùng
    serializer_class = UserSerializer  # Dùng UserSerializer để tạo mới người dùng
class UserUpdateAPIView(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'id'  # Tìm người dùng theo id
class UserDeleteAPIView(generics.DestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'id'  # Tìm người dùng theo id
    
class LevelListAPIView(generics.ListAPIView):
    queryset = Level.objects.all()  # Lấy tất cả các level
    serializer_class = LevelSerializer  # Sử dụng LevelSerializer để trả về dữ liệu
    

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