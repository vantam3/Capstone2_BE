from django.db import models
from django.conf import settings
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
    level = models.ForeignKey(Level, on_delete=models.SET_NULL, null=True, blank=True) # Liên kết với Level, SET_NULL nếu level bị xóa

    def __str__(self):
        return self.title


# Bảng để lưu âm thanh của từng đoạn văn mẫu
class Audio(models.Model):
    speaking_text = models.ForeignKey(SpeakingText, on_delete=models.CASCADE, related_name='audio_files')  # Liên kết với đoạn văn mẫu
    audio_file = models.FileField(upload_to='audio_files/')  # Lưu trữ tệp âm thanh trong thư mục 'audio_files'

    def __str__(self):
        return f"Audio for {self.speaking_text.title}"

# Bảng để lưu lịch sử luyện tập của người dùng
class UserPracticeLog(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='practice_logs' # Giúp truy cập logs từ đối tượng user: user.practice_logs.all()
    )
    # Liên kết với bài nói đã được luyện tập (Optional)
    speaking_text = models.ForeignKey(
        SpeakingText,
        on_delete=models.SET_NULL, # Giữ log nếu text bị xóa
        related_name='practice_logs',
        null=True, blank=True # Cho phép log không gắn với SpeakingText cụ thể (nếu dùng câu tùy chỉnh)
    )
    # Thêm trường để lưu câu gốc được sử dụng trong lần luyện tập này
    reference_text = models.TextField(
        null=True, blank=True,
        help_text="The exact reference text used for this practice session."
    )
    # Thêm trường để lưu văn bản được STT chuyển đổi
    transcribed_text = models.TextField(
        null=True, blank=True,
        help_text="Text transcribed from the user's audio."
    )
    # Thời điểm thực hiện luyện tập
    practice_date = models.DateTimeField(auto_now_add=True)
    # Điểm số tổng thể đạt được
    score = models.FloatField(
        null=True, blank=True,
        help_text="Overall pronunciation score (e.g., 0-100)"
    )
    # Lưu trữ chi tiết kết quả đánh giá
    details = models.JSONField(
        null=True, blank=True,
        help_text="Detailed assessment results, including word/phoneme errors, scores (accuracy, fluency), and error positions."
        # Ví dụ cấu trúc:
        # {
        #   "pronunciation_score": 85.0,
        #   "accuracy_score": 88.0,
        #   "fluency_score": 82.0,
        #   "completeness_score": 95.0,
        #   "words": [
        #      {"word": "hello", "accuracy_score": 100.0, "error_type": "None", "offset": 0, "duration": 500},
        #      {"word": "world", "accuracy_score": 70.0, "error_type": "Mispronunciation", "offset": 600, "duration": 600, "phonemes": [...]},
        #      ...
        #   ],
        #   "errors_for_highlighting": [
        #       {"word": "world", "start_index": 6, "end_index": 11, "error_type": "Mispronunciation"}
        #   ]
        # }
    )

    class Meta:
        ordering = ['-practice_date'] # Sắp xếp mặc định theo ngày mới nhất lên đầu
        verbose_name = "User Practice Log"
        verbose_name_plural = "User Practice Logs"

    def __str__(self):
        score_display = f"Score: {self.score}" if self.score is not None else "No score"
        text_title = self.speaking_text.title if self.speaking_text else "Custom Text" # Hiển thị tiêu đề hoặc 'Custom Text'
        return f"{self.user.get_username()} practiced '{text_title}' on {self.practice_date.strftime('%Y-%m-%d %H:%M')} - {score_display}"

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