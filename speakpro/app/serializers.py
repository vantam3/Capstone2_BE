from rest_framework import serializers
from rest_framework.serializers import Serializer, CharField
from django.contrib.auth.models import User
from .models import Genre, SpeakingText, Audio, UserPracticeLog, Level, UserAudio, SpeakingResult
import base64
import decimal # Thêm import decimal

class ResetPasswordSerializer(Serializer):
    email = CharField(required=True)
    confirmation_code = CharField(required=True)
    new_password = CharField(required=True)

class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    confirm_password = serializers.CharField(required=True)

# Serializer đơn giản cho SpeakingText để lồng vào lịch sử
class SimpleSpeakingTextSerializer(serializers.ModelSerializer):
    genre_name = serializers.CharField(source='genre.name', read_only=True)
    level_name = serializers.CharField(source='level.name', read_only=True, allow_null=True) # Thêm level name

    class Meta:
        model = SpeakingText
        fields = ['id', 'title', 'genre_name', 'level_name', 'language'] # Thêm level_name

# Serializer cho UserPracticeLog (ĐÃ CẬP NHẬT)
class UserPracticeLogSerializer(serializers.ModelSerializer):
    # Khi hiển thị lịch sử (GET), chúng ta muốn thấy chi tiết bài nói (nếu có)
    speaking_text_details = SimpleSpeakingTextSerializer(source='speaking_text', read_only=True)
    # Khi tạo log mới (POST), frontend có thể gửi ID của bài nói (tùy chọn)
    speaking_text_id = serializers.PrimaryKeyRelatedField(
        queryset=SpeakingText.objects.all(),
        source='speaking_text', # Map field này với 'speaking_text' của model
        write_only=True, # Field này chỉ dùng để ghi
        required=False, # Không bắt buộc nếu cung cấp reference_text
        allow_null=True
    )
    # Hiển thị username của người dùng trong lịch sử (read-only)
    username = serializers.CharField(source='user.username', read_only=True)
    # Định dạng lại ngày tháng cho dễ đọc hơn
    practice_date = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
    # reference_text và transcribed_text là một phần của model, sẽ được bao gồm trong fields
    # details (JSONField) cũng sẽ được bao gồm

    class Meta:
        model = UserPracticeLog
        fields = [
            'id',
            'username', # Hiển thị username
            'speaking_text_id', # Chỉ dùng để POST (write_only, optional)
            'speaking_text_details', # Chỉ dùng để GET (read_only)
            'reference_text', # Câu gốc đã dùng (GET/POST)
            'transcribed_text', # Văn bản STT (read_only)
            'practice_date',
            'score', # Điểm tổng thể
            'details' # Kết quả đánh giá chi tiết JSON
        ]
        read_only_fields = ('id', 'username', 'practice_date', 'speaking_text_details', 'transcribed_text')

    def validate_score(self, value):
        # Validate score từ 0 đến 100
        if value is not None:
            try:
                score_decimal = decimal.Decimal(str(value))
                if not (decimal.Decimal(0) <= score_decimal <= decimal.Decimal(100)):
                    raise serializers.ValidationError("Score must be between 0 and 100.")
            except decimal.InvalidOperation:
                 raise serializers.ValidationError("Score must be a valid number.")
        return value

    def validate(self, data):
        # Đảm bảo có speaking_text_id hoặc reference_text khi tạo mới
        if not data.get('speaking_text') and not data.get('reference_text'):
            raise serializers.ValidationError("Either 'speaking_text_id' or 'reference_text' must be provided when creating a log.")
        return data

# Serializer cho Genre
class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ['id', 'name']

# Serializer cho Level
class LevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Level
        fields = ['id', 'name']  # Trả về id và name của mỗi level

# Serializer cho SpeakingText
class SpeakingTextSerializer(serializers.ModelSerializer):
    # Hiển thị thông tin chi tiết của Genre và Level thay vì chỉ ID
    genre = GenreSerializer(read_only=True)
    level = LevelSerializer(read_only=True, allow_null=True)
    # Thêm các field write-only để nhận ID khi tạo/cập nhật
    genre_id = serializers.PrimaryKeyRelatedField(
        queryset=Genre.objects.all(), source='genre', write_only=True
    )
    level_id = serializers.PrimaryKeyRelatedField(
        queryset=Level.objects.all(), source='level', write_only=True, allow_null=True, required=False
    )
    # Xử lý content (BinaryField)
    content = serializers.SerializerMethodField()
    content_input = serializers.CharField(write_only=True, required=False, help_text="Text content to be saved (will be hex-encoded).")

    class Meta:
        model = SpeakingText
        fields = [
            'id', 'title',
            'genre', 'level', # Read-only nested serializers
            'genre_id', 'level_id', # Write-only fields for IDs
            'content', # Read-only processed content
            'content_input', # Write-only raw text content
            'language'
        ]
        read_only_fields = ('content',) # content được tạo từ get_content

    def get_content(self, obj):
        """Decodes hex-encoded binary content back to UTF-8 text for display."""
        if obj.content:
            try:
                # Giả sử content được lưu dưới dạng hex string của UTF-8 bytes
                content_hex = obj.content.decode('utf-8') # Decode binary field (bytes) to hex string
                content_binary = bytes.fromhex(content_hex) # Decode hex string to original bytes
                return content_binary.decode('utf-8') # Decode original bytes to text
            except (UnicodeDecodeError, ValueError, AttributeError, TypeError) as e:
                print(f"Error decoding content for SpeakingText ID {obj.id}: {e}")
                return "[Content Decoding Error]"
        return None # Hoặc ""

    def create(self, validated_data):
        """Encodes text input to hex-encoded binary before saving."""
        content_input_text = validated_data.pop('content_input', None)
        instance = super().create(validated_data)
        if content_input_text:
            try:
                content_binary = content_input_text.encode('utf-8') # Text to bytes
                content_hex = content_binary.hex() # Bytes to hex string
                instance.content = content_hex.encode('utf-8') # Store hex string as bytes in BinaryField
                instance.save(update_fields=['content'])
            except Exception as e:
                 print(f"Error encoding content for SpeakingText ID {instance.id}: {e}")
                 # Decide how to handle encoding errors (e.g., log, raise exception, save without content)
        return instance

    def update(self, instance, validated_data):
        """Handles encoding for updates as well."""
        content_input_text = validated_data.pop('content_input', None)
        instance = super().update(instance, validated_data)
        if content_input_text is not None: # Allow updating content to empty
            if content_input_text:
                try:
                    content_binary = content_input_text.encode('utf-8')
                    content_hex = content_binary.hex()
                    instance.content = content_hex.encode('utf-8')
                except Exception as e:
                    print(f"Error encoding content during update for SpeakingText ID {instance.id}: {e}")
                    instance.content = None # Or handle error differently
            else:
                 instance.content = None # Set content to None if input is empty string
            instance.save(update_fields=['content'])
        return instance

# Serializer cho Audio
class AudioSerializer(serializers.ModelSerializer):
    audio_file = serializers.SerializerMethodField()

    class Meta:
        model = Audio
        fields = ['id', 'speaking_text', 'audio_file']

    def get_audio_file(self, obj):
        request = self.context.get('request')
        if obj.audio_file and request:
            return request.build_absolute_uri(obj.audio_file.url) # Trả về URL tuyệt đối
        elif obj.audio_file:
             return obj.audio_file.url # Trả về URL tương đối nếu không có request context
        return None

# Serializer cho UserAudio
class UserAudioSerializer(serializers.ModelSerializer):
    audio_file = serializers.SerializerMethodField()

    class Meta:
        model = UserAudio
        fields = ['id', 'user', 'audio_file', 'uploaded_at']
        read_only_fields = ('user', 'uploaded_at') # Thường user được gán tự động

    def get_audio_file(self, obj):
        request = self.context.get('request')
        if obj.audio_file and request:
            return request.build_absolute_uri(obj.audio_file.url)
        elif obj.audio_file:
            return obj.audio_file.url
        return None

# Serializer cho User (Django's built-in User model)
class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False) # Thêm password field

    class Meta:
        model = User
        # Bao gồm các trường cần thiết, loại bỏ password khỏi fields đọc
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'is_active', 'is_staff', 'is_superuser', 'date_joined', 'password']
        read_only_fields = ('is_staff', 'is_superuser', 'date_joined')

    # Mã hóa mật khẩu khi tạo hoặc cập nhật user
    def create(self, validated_data):
        user = User.objects.create_user(**validated_data) # Sử dụng create_user để hash password
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        # Cập nhật các trường khác bình thường
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if password:
            instance.set_password(password) # Hash password mới nếu có

        instance.save()
        return instance

# Serializer cho SpeakingResult (Có thể không cần nếu dùng UserPracticeLog)
class SpeakingResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = SpeakingResult
        fields = ['id', 'speaking_text', 'user_text', 'score', 'timestamp']


# --- Serializers for Pronunciation Assessment (MỚI) ---

class PronunciationAssessmentInputSerializer(serializers.Serializer):
    # FileField không hoạt động tốt trong Serializer cho input đơn giản,
    # file thường được xử lý trực tiếp từ request.FILES trong view.
    # audio_file = serializers.FileField(required=True) # Chỉ để minh họa
    reference_text = serializers.CharField(required=True, trim_whitespace=True)
    speaking_text_id = serializers.IntegerField(required=False, allow_null=True) # Optional: ID nếu luyện theo bài có sẵn

    def validate_reference_text(self, value):
        if not value:
            raise serializers.ValidationError("Reference text cannot be empty.")
        # Thêm các validation khác nếu cần (ví dụ: chỉ cho phép ký tự tiếng Anh)
        return value

class PronunciationErrorSerializer(serializers.Serializer):
    """Serializer for individual pronunciation errors."""
    word = serializers.CharField(help_text="The word/segment with the error.")
    start_index = serializers.IntegerField(help_text="Start index of the error in the reference text.")
    end_index = serializers.IntegerField(help_text="End index of the error in the reference text.")
    error_type = serializers.CharField(required=False, allow_null=True, help_text="Type of error (e.g., Mispronunciation, Insertion, Deletion).")
    suggestion = serializers.CharField(required=False, allow_null=True, help_text="Suggestion for correction.")


class PronunciationAssessmentResultSerializer(serializers.Serializer):
    """Serializer for the overall pronunciation assessment result."""
    pronunciation_score = serializers.FloatField(allow_null=True, help_text="Overall pronunciation score (0-100).")
    transcribed_text = serializers.CharField(required=False, allow_null=True, help_text="Text transcribed from user audio.")
    reference_text = serializers.CharField(help_text="The reference text used for comparison.")
    errors = PronunciationErrorSerializer(many=True, help_text="List of identified pronunciation errors with their positions.")
    # Có thể thêm các điểm chi tiết khác nếu có từ dịch vụ đánh giá
    accuracy_score = serializers.FloatField(required=False, allow_null=True)
    fluency_score = serializers.FloatField(required=False, allow_null=True)
    completeness_score = serializers.FloatField(required=False, allow_null=True)