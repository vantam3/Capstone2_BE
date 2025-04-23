from django.db import models
from django.contrib.auth.models import User

# Bảng để lưu thông tin thể loại
class Genre(models.Model):
    name = models.CharField(max_length=100, unique=True)  # Tên thể loại (ví dụ: truyện, hội thoại, thuyết trình,...)

    def __str__(self):
        return self.name

class Level(models.Model):
    name = models.CharField(max_length=50, unique=True)  # Tên mức độ, ví dụ: "beginner", "intermediate", "advanced"

    def __str__(self):
        return self.name
# Bảng để lưu thông tin các đoạn văn mẫu
class SpeakingText(models.Model):
    title = models.CharField(max_length=255)  # Tiêu đề của đoạn văn mẫu
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE, related_name='speaking_texts')  # Liên kết với thể loại
    content = models.BinaryField(null=True)  # Lưu nội dung của đoạn văn mẫu dưới dạng binary
    language = models.CharField(max_length=50, null=True, blank=True)  # Ngôn ngữ của văn bản
    level = models.ForeignKey(Level, on_delete=models.CASCADE, null=True)  # Liên kết với Level qua ForeignKey

    def __str__(self):
        return self.title


# Bảng để lưu âm thanh của từng đoạn văn mẫu
class Audio(models.Model):
    speaking_text = models.ForeignKey(SpeakingText, on_delete=models.CASCADE, related_name='audio_files')  # Liên kết với đoạn văn mẫu
    audio_file = models.FileField(upload_to='audio_files/')  # Lưu trữ tệp âm thanh trong thư mục 'audio_files'

    def __str__(self):
        return f"Audio for {self.speaking_text.title}"
    
class UserAudio(models.Model):
    # Liên kết với người dùng
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="audio_files")
    
    # Lưu trữ tệp âm thanh
    audio_file = models.FileField(upload_to='user_audio/', null=True, blank=True)

    # Lưu trữ thông tin thêm nếu cần
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Audio file of {self.user.username} uploaded at {self.uploaded_at}"
# Bảng để lưu kết quả ghi âm và so sánh
class SpeakingResult(models.Model):
    speaking_text = models.ForeignKey(SpeakingText, on_delete=models.CASCADE, related_name='speaking_results')  # Liên kết với đoạn văn mẫu
    user_text = models.TextField()  # Văn bản người dùng đã chuyển đổi từ giọng nói
    score = models.DecimalField(max_digits=5, decimal_places=2)  # Điểm so sánh giữa văn bản người dùng và văn bản gốc
    timestamp = models.DateTimeField(auto_now_add=True)  # Thời gian người dùng thực hiện

    def __str__(self):
        return f"Result for {self.speaking_text.title} - Score: {self.score}"