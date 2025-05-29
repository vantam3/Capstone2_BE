from rest_framework import serializers
from .models import Genre, SpeakingText, Audio, UserAudio, SpeakingResult, Level, Challenge, User, UserChallengeProgress, ChallengeExercise, UserExerciseAttempt
from django.contrib.auth.models import User
from rest_framework.serializers import Serializer, CharField
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
                return obj.content.decode('utf-8')  # GIẢI MÃ trực tiếp BinaryField
            except (UnicodeDecodeError, ValueError):
                return "Không thể giải mã nội dung, dữ liệu không phải văn bản hợp lệ."
        return "Không có nội dung."




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
# password serializer
class ResetPasswordSerializer(Serializer):
    email = CharField(required=True)
    confirmation_code = CharField(required=True)
    new_password = CharField(required=True)
class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    confirm_password = serializers.CharField(required=True)

# challenge serializer
class ChallengeExerciseSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChallengeExercise
        fields = ['id', 'title', 'description', 'order']

class ChallengeExerciseDetailSerializer(serializers.ModelSerializer):
    speaking_text_content = serializers.SerializerMethodField()
    challenge_id = serializers.IntegerField(source='challenge.id', read_only=True)

    class Meta:
        model = ChallengeExercise
        fields = [
            'id',
            'title',
            'description',
            'order',
            'speaking_text_content',
            'challenge_id',
            'created_at',
            'updated_at'
        ]

    def get_speaking_text_content(self, obj):
        if obj.speaking_text_content:
            try:
                hex_string_representation = obj.speaking_text_content.decode('utf-8')
                actual_binary_data = bytes.fromhex(hex_string_representation)
                return actual_binary_data.decode('utf-8')
            except (UnicodeDecodeError, ValueError, AttributeError) as e:
                print(f"Error decoding speaking_text_content for exercise ID {obj.id} (Title: '{obj.title}'): {str(e)}")
                return "Không thể giải mã nội dung, dữ liệu không phải văn bản hợp lệ."
        return "Không có nội dung."

class ChallengeSerializer(serializers.ModelSerializer):
    exercises = ChallengeExerciseSerializer(many=True, read_only=True)
    days_left = serializers.SerializerMethodField()

    class Meta:
        model = Challenge
        fields = ['id', 'title', 'description', 'is_featured', 'difficulty', 'reward_points', 
                  'start_date', 'end_date', 'participant_count', 'level', 'days_left', 'exercises']

    def get_days_left(self, obj):
        from datetime import datetime
        delta = obj.end_date - datetime.now(obj.end_date.tzinfo)
        return f"{delta.days} days left" if delta.days > 0 else "Ended"

class UserChallengeProgressSerializer(serializers.ModelSerializer):
    challenge = ChallengeSerializer()
    class Meta:
        model = UserChallengeProgress
        fields = ['id', 'challenge', 'score', 'completion_percentage', 'status', 'last_attempted_date', 'completed_date']

class ExerciseHistorySerializer(serializers.ModelSerializer):
    title = serializers.CharField(source='challenge_exercise.title')
    challenge_title = serializers.CharField(source='challenge_exercise.challenge.title')
    attempted_time = serializers.SerializerMethodField()

    class Meta:
        model = UserExerciseAttempt
        fields = ['id', 'title', 'challenge_title', 'score', 'attempted_time']

    def get_attempted_time(self, obj):
        return obj.attempted_at.strftime("%Y-%m-%d %H:%M:%S")