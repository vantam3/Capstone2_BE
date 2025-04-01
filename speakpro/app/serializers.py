from rest_framework import serializers
from .models import Genre, SpeakingText, Audio

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

