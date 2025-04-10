from rest_framework import serializers
from rest_framework.serializers import Serializer, CharField
from django.contrib.auth.models import User
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
# Serializer cho Genre
class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ['id', 'name']

class SpeakingTextSerializer(serializers.ModelSerializer):
    genre = GenreSerializer()  # Nested genre
    content = serializers.SerializerMethodField()  # Chuyển đổi BinaryField thành văn bản

    class Meta:
        model = SpeakingText
        fields = ['id', 'title', 'genre', 'content', 'language']

    def get_content(self, obj):
        if obj.content:
            try:
                # Chuyển đổi chuỗi hex thành bytes
                hex_content = obj.content.decode('utf-8')  # Giải mã nội dung nhị phân thành chuỗi UTF-8
                # Chuyển đổi hex string thành văn bản
                byte_content = bytes.fromhex(hex_content)
                return byte_content.decode('utf-8')  # Giải mã lại thành văn bản
            except (UnicodeDecodeError, ValueError):
                return "Không thể giải mã nội dung."
        return "Không có nội dung."


from rest_framework import serializers
from .models import Audio

class AudioSerializer(serializers.ModelSerializer):
    audio_file = serializers.SerializerMethodField()

    class Meta:
        model = Audio
        fields = ['id', 'speaking_text', 'audio_file']

    def get_audio_file(self, obj):
        # Trả về đường dẫn tương đối của tệp âm thanh
        return obj.audio_file.url

