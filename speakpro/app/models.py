from django.db import models
from django.conf import settings

# Bảng để lưu thông tin thể loại
class Genre(models.Model):
    name = models.CharField(max_length=100, unique=True)  # Tên thể loại (ví dụ: truyện, hội thoại, thuyết trình,...)

    def __str__(self):
        return self.name


# Bảng để lưu thông tin các đoạn văn mẫu
class SpeakingText(models.Model):
    title = models.CharField(max_length=255)  # Tiêu đề của đoạn văn mẫu
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE, related_name='speaking_texts')  # Liên kết với thể loại
    content = models.BinaryField(null=True)  # Lưu nội dung của đoạn văn mẫu dưới dạng binary
    language = models.CharField(max_length=50, null=True, blank=True)  # Ngôn ngữ của văn bản

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
    # Liên kết với bài nói đã được luyện tập
    speaking_text = models.ForeignKey(
        SpeakingText,
        on_delete=models.CASCADE, # Hoặc models.SET_NULL nếu muốn giữ log khi bài nói bị xóa
        related_name='practice_logs'
    )
    # Thời điểm thực hiện luyện tập
    practice_date = models.DateTimeField(auto_now_add=True)
    # Điểm số đạt được 
    score = models.FloatField(null=True, blank=True, help_text="Pronunciation score (e.g., 0-100)")
    # Lưu trữ chi tiết khác về luyện tập, có thể là phản hồi từ hệ thống hoặc lỗi phát hiện được
    details = models.JSONField(null=True, blank=True, help_text="Detailed feedback or identified errors in JSON format")
    # details = models.TextField(null=True, blank=True, help_text="Detailed feedback or identified errors") # Alternative

    class Meta:
        ordering = ['-practice_date'] # Sắp xếp mặc định theo ngày mới nhất lên đầu
        verbose_name = "User Practice Log"
        verbose_name_plural = "User Practice Logs"
        # Đảm bảo user và speaking_text cùng nhau có thể xuất hiện nhiều lần (mỗi lần luyện tập)

    def __str__(self):
        score_display = f"Score: {self.score}" if self.score is not None else "No score"
        return f"{self.user.get_username()} practiced '{self.speaking_text.title}' on {self.practice_date.strftime('%Y-%m-%d %H:%M')} - {score_display}"
