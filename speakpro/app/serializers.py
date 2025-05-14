from rest_framework import serializers
from .models import Genre, SpeakingText, Audio, UserAudio, SpeakingResult, Level
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

class ResetPasswordSerializer(Serializer):
    email = CharField(required=True)
    confirmation_code = CharField(required=True)
    new_password = CharField(required=True)
class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    confirm_password = serializers.CharField(required=True)