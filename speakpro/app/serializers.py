from rest_framework import serializers
from rest_framework.serializers import Serializer, CharField
from django.contrib.auth.models import User
from django.utils import timezone 
from .models import ( 
    Genre, SpeakingText, Audio, UserPracticeLog, Level, UserAudio, SpeakingResult,
    ChallengeCategory, Challenge, ChallengeExercise, 
    UserChallengeAttempt, UserChallengeExerciseAttempt, UserChallengeStreak, 
    Achievement, UserAchievement
)
class ResetPasswordSerializer(Serializer):
    email = CharField(required=True)
    confirmation_code = CharField(required=True)
    new_password = CharField(required=True)
class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    confirm_password = serializers.CharField(required=True)
from .models import Genre, SpeakingText, Audio, UserPracticeLog

# Serializer đơn giản cho SpeakingText để lồng vào lịch sử 
class SimpleSpeakingTextSerializer(serializers.ModelSerializer):
    genre_name = serializers.CharField(source='genre.name', read_only=True)

    class Meta:
        model = SpeakingText
        fields = ['id', 'title', 'genre_name', 'language']

# Serializer cho UserPracticeLog
class UserPracticeLogSerializer(serializers.ModelSerializer):
    # Khi hiển thị lịch sử (GET), chúng ta muốn thấy chi tiết bài nói
    speaking_text_details = SimpleSpeakingTextSerializer(source='speaking_text', read_only=True)
    # Khi tạo log mới (POST), frontend chỉ cần gửi ID của bài nói
    speaking_text_id = serializers.PrimaryKeyRelatedField(
        queryset=SpeakingText.objects.all(),
        source='speaking_text', # Map field này với 'speaking_text' của model
        write_only=True # Field này chỉ dùng để ghi, không hiển thị khi đọc
    )
    # Hiển thị username của người dùng trong lịch sử (read-only)
    username = serializers.CharField(source='user.username', read_only=True)
    # Định dạng lại ngày tháng cho dễ đọc hơn
    practice_date = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)

    class Meta:
        model = UserPracticeLog
        fields = [
            'id',
            'username', # Hiển thị username thay vì user_id
            'speaking_text_id', # Chỉ dùng để POST (write_only)
            'speaking_text_details', # Chỉ dùng để GET (read_only)
            'practice_date',
            'score',
            'details'
        ]
        read_only_fields = ('id', 'username', 'practice_date', 'speaking_text_details')
    def validate_score(self, value):
        if value is not None and not (0 <= value <= 100): # Kiểm tra xem điểm có nằm trong khoảng 0-100 không
            raise serializers.ValidationError("Score must be between 0 and 100.")
        return value
from .models import Genre, SpeakingText, Audio, UserAudio, SpeakingResult, Level
from django.contrib.auth.models import User
from rest_framework import serializers
import base64
# Serializer cho Genre
class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ['id', 'name']
        
class LevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Level
        fields = ['id', 'name']  # Trả về ID và tên của mức độ
class LevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Level
        fields = ['id', 'name']  # Trả về id và name của mỗi level

class SpeakingTextSerializer(serializers.ModelSerializer):
    genre = serializers.PrimaryKeyRelatedField(queryset=Genre.objects.all())  # Liên kết với genre qua ID
    level = serializers.PrimaryKeyRelatedField(queryset=Level.objects.all())  # Liên kết với level qua ID
    content = serializers.SerializerMethodField()  # Chuyển đổi BinaryField thành văn bản

    class Meta:
        model = SpeakingText
        fields = ['id', 'title', 'genre', 'content', 'language', 'level']  # Bao gồm level và content

    def get_content(self, obj):
   
        if obj.content:
            try:
                # Giải mã từ hex thành binary
                content_binary = bytes.fromhex(obj.content.decode('utf-8'))  # Chuyển đổi từ hex thành binary
                
                # Giải mã nhị phân (binary) thành văn bản (UTF-8)
                return content_binary.decode('utf-8')  # Chuyển đổi từ binary thành văn bản
            except (UnicodeDecodeError, ValueError):
                return "Không thể giải mã nội dung, dữ liệu không phải văn bản hợp lệ."  # Trường hợp lỗi nếu không thể giải mã nội dung
        return "Không có nội dung."  # Trả về chuỗi mặc định nếu không có nội dung



class AudioSerializer(serializers.ModelSerializer):
    audio_file = serializers.SerializerMethodField()

    class Meta:
        model = Audio
        fields = ['id', 'speaking_text', 'audio_file']

    def get_audio_file(self, obj):
        # Trả về đường dẫn tương đối của tệp âm thanh
        if obj.audio_file:
            return obj.audio_file.url  # Trả về URL của tệp âm thanh
        return None  # Trường hợp không có tệp âm thanh

class UserAudioSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAudio
        fields = ['id', 'user', 'audio_file', 'uploaded_at']
        
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'is_active', 'date_joined']
    # Mã hóa mật khẩu trước khi lưu vào cơ sở dữ liệu
    def create(self, validated_data):
        password = validated_data.pop('password', None)
        user = User.objects.create(**validated_data)
        if password:
            user.set_password(password)  # Mã hóa mật khẩu
            user.save()
        return user
class SpeakingResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = SpeakingResult
        fields = ['speaking_text', 'user_text', 'score', 'timestamp']

####### Challenges serializers #######
class ChallengeCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ChallengeCategory
        fields = ['id', 'name', 'description']

class SimpleSpeakingTextForExerciseSerializer(serializers.ModelSerializer):
    """Serializer rút gọn cho SpeakingText để lồng vào ChallengeExercise."""
    genre_name = serializers.CharField(source='genre.name', read_only=True)
    level_name = serializers.CharField(source='level.name', read_only=True)
    # Loại bỏ get_content nếu đã sửa model SpeakingText.content thành TextField
    # Và content được lấy trực tiếp
    class Meta:
        model = SpeakingText
        fields = ['id', 'title', 'content', 'language', 'genre_name', 'level_name']


class ChallengeExerciseSerializer(serializers.ModelSerializer):
    speaking_text_details = SimpleSpeakingTextForExerciseSerializer(source='speaking_text', read_only=True)
    # speaking_text_id = serializers.PrimaryKeyRelatedField(
    #     queryset=SpeakingText.objects.all(), source='speaking_text', write_only=True
    # )

    class Meta:
        model = ChallengeExercise
        fields = ['id', 'order', 'speaking_text_details'] # 'speaking_text_id' nếu cần write


class UserChallengeExerciseAttemptSerializer(serializers.ModelSerializer):
    exercise_title = serializers.CharField(source='challenge_exercise.speaking_text.title', read_only=True)
    # Lấy score và details từ UserPracticeLog nếu có
    score = serializers.SerializerMethodField()
    practice_details = serializers.SerializerMethodField()

    class Meta:
        model = UserChallengeExerciseAttempt
        fields = ['id', 'challenge_exercise', 'exercise_title', 'is_completed', 'completed_at', 'score', 'practice_details', 'user_practice_log']
        read_only_fields = ['score_at_completion']


    def get_score(self, obj):
        if obj.user_practice_log:
            return obj.user_practice_log.score
        return obj.score_at_completion # Fallback nếu user_practice_log bị xóa/không có

    def get_practice_details(self, obj):
        if obj.user_practice_log:
            return obj.user_practice_log.details
        return None

class UserChallengeAttemptSerializer(serializers.ModelSerializer):
    challenge_title = serializers.CharField(source='challenge.title', read_only=True)
    challenge_description = serializers.CharField(source='challenge.description', read_only=True)
    total_exercises = serializers.SerializerMethodField()
    completed_exercises = serializers.SerializerMethodField()
    progress_percentage = serializers.SerializerMethodField()
    # exercises_status = UserChallengeExerciseAttemptSerializer(source='exercise_attempts', many=True, read_only=True) # Nếu muốn trả về chi tiết từng exercise attempt

    class Meta:
        model = UserChallengeAttempt
        fields = [
            'id', 'user', 'challenge', 'challenge_title', 'challenge_description', 
            'status', 'points_earned', 'started_at', 'completed_at',
            'total_exercises', 'completed_exercises', 'progress_percentage',
            # 'exercises_status'
        ]
        read_only_fields = ['user', 'points_earned', 'started_at', 'completed_at', 'total_exercises', 'completed_exercises', 'progress_percentage']

    def get_total_exercises(self, obj):
        return obj.challenge.exercises.count()

    def get_completed_exercises(self, obj):
        return obj.exercise_attempts.filter(is_completed=True).count()

    def get_progress_percentage(self, obj):
        total = self.get_total_exercises(obj)
        completed = self.get_completed_exercises(obj)
        if total > 0:
            return round((completed / total) * 100, 2)
        return 0


class ChallengeSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True, allow_null=True)
    level_name = serializers.CharField(source='level.name', read_only=True, allow_null=True)
    exercises = ChallengeExerciseSerializer(many=True, read_only=True) # Danh sách các bài tập
    participant_count = serializers.SerializerMethodField()
    time_remaining_seconds = serializers.SerializerMethodField()
    user_progress = serializers.SerializerMethodField() # Thông tin tiến trình của user hiện tại (nếu có)

    class Meta:
        model = Challenge
        fields = [
            'id', 'title', 'description', 'category', 'category_name', 'level', 'level_name',
            'points_reward', 'start_date', 'end_date', 'duration_days',
            'is_featured', 'is_active', 'exercises', 'participant_count',
            'time_remaining_seconds', 'user_progress'
        ]
        # Thêm 'level' và 'category' vào đây nếu frontend cần gửi ID khi tạo/update Challenge
        # read_only_fields for GET, or make them writeable if needed for POST/PUT
    
    def get_participant_count(self, obj):
        # Đếm số UserChallengeAttempt cho challenge này
        return UserChallengeAttempt.objects.filter(challenge=obj).count()

    def get_time_remaining_seconds(self, obj):
        if not obj.get_is_currently_active:
            return 0
        
        now = timezone.now()
        
        # Ưu tiên end_date nếu có
        if obj.end_date:
            if obj.end_date > now:
                return int((obj.end_date - now).total_seconds())
            return 0 # Đã kết thúc

        # Nếu không có end_date nhưng có duration_days
        if obj.duration_days:
            # Giả sử date_created tồn tại, hoặc lấy start_date
            effective_start_date = obj.start_date if obj.start_date else obj.date_created # Cần đảm bảo date_created tồn tại trên model Challenge
            
            if not effective_start_date: # Nếu không xác định được ngày bắt đầu để tính duration
                return None # Hoặc một giá trị lớn nếu challenge không bao giờ hết hạn theo duration

            challenge_actual_end_date = effective_start_date + timezone.timedelta(days=obj.duration_days)
            if challenge_actual_end_date > now:
                return int((challenge_actual_end_date - now).total_seconds())
            return 0 # Đã kết thúc theo duration
            
        return None # Không có end_date và duration_days, xem như không giới hạn thời gian

    def get_user_progress(self, obj):
        request = self.context.get('request')
        if request and hasattr(request, 'user') and request.user.is_authenticated:
            try:
                attempt = UserChallengeAttempt.objects.get(user=request.user, challenge=obj)
                return UserChallengeAttemptSerializer(attempt, context=self.context).data
            except UserChallengeAttempt.DoesNotExist:
                return None
        return None


class UserChallengeStreakSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserChallengeStreak
        fields = ['user', 'current_streak_days', 'longest_streak_days', 'last_challenge_completed_date']
        read_only_fields = fields


class AchievementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Achievement
        fields = ['id', 'name', 'description', 'icon_url', 'achievement_type', 'criteria', 'points_reward']

class UserAchievementSerializer(serializers.ModelSerializer):
    achievement_details = AchievementSerializer(source='achievement', read_only=True)

    class Meta:
        model = UserAchievement
        fields = ['id', 'user', 'achievement', 'achievement_details', 'achieved_at']
        read_only_fields = ['user', 'achieved_at', 'achievement_details']


# Serializer cho Leaderboard
class ChallengeLeaderboardUserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username')
    # avatar_url = serializers.ImageField(source='user.profile.avatar', read_only=True) # Nếu có model Profile với avatar

    class Meta:
        model = User
        fields = ['id', 'username'] # Thêm avatar nếu có

class ChallengeLeaderboardEntrySerializer(serializers.ModelSerializer):
    user_info = ChallengeLeaderboardUserSerializer(source='user', read_only=True)
    rank = serializers.IntegerField(read_only=True, allow_null=True) # Sẽ được thêm vào từ view

    class Meta:
        model = UserChallengeAttempt
        fields = ['user_info', 'points_earned', 'completed_at', 'status', 'rank']


####### Leaderboard serializers #######
class GlobalLeaderboardUserSerializer(serializers.ModelSerializer):
    """Serializer cho thông tin user trên Global Leaderboard."""
    avatar_initials = serializers.SerializerMethodField()
    # description = serializers.CharField(source='userprofile.description', read_only=True, allow_null=True) # Nếu có UserProfile

    class Meta:
        model = User
        fields = ['id', 'username', 'avatar_initials'] # Thêm 'description' nếu có

    def get_avatar_initials(self, obj):
        if obj.first_name and obj.last_name:
            return (obj.first_name[0] + obj.last_name[0]).upper()
        elif obj.username:
            return obj.username[0:2].upper()
        return "AA"


class GlobalLeaderboardEntrySerializer(serializers.Serializer): # Không kế thừa ModelSerializer vì dữ liệu được tổng hợp
    rank = serializers.IntegerField()
    user = GlobalLeaderboardUserSerializer() # Thông tin user lồng vào
    total_points = serializers.IntegerField()
    current_streak_days = serializers.IntegerField()
    # trend_percentage = serializers.FloatField(allow_null=True) # Cho điểm trend

    # class Meta: # Không cần Meta class vì không map trực tiếp với model
    #     fields = ['rank', 'user', 'total_points', 'current_streak_days', 'trend_percentage']


class UserRankingStatsSerializer(serializers.Serializer):
    current_rank = serializers.IntegerField(allow_null=True)
    total_learners = serializers.IntegerField()
    points_to_next_tier = serializers.IntegerField(allow_null=True)
    # Thêm các thông tin khác nếu cần cho phần "Your Ranking"
    user_total_points = serializers.IntegerField()
    user_current_streak_days = serializers.IntegerField()