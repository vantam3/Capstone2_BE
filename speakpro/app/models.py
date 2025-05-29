from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

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
    audio_file = models.FileField(upload_to='file_audio/')  # Lưu trữ tệp âm thanh trong thư mục 'audio_files'

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
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    speaking_text = models.ForeignKey(SpeakingText, on_delete=models.CASCADE, related_name='speaking_results')  # Liên kết với đoạn văn mẫu
    user_text = models.TextField()  # Văn bản người dùng đã chuyển đổi từ giọng nói
    score = models.DecimalField(max_digits=5, decimal_places=2)  # Điểm so sánh giữa văn bản người dùng và văn bản gốc
    timestamp = models.DateTimeField(auto_now_add=True)  # Thời gian người dùng thực hiện

    def __str__(self):
        return f"Result for {self.speaking_text.title} - Score: {self.score}"
    
# Bảng để lưu thử thách
class Challenge(models.Model):
    DIFFICULTY_CHOICES = [('easy', 'Easy'), ('medium', 'Medium'), ('hard', 'Hard')]

    title = models.CharField(max_length=255)
    description = models.TextField()
    is_featured = models.BooleanField(default=False)
    difficulty = models.CharField(max_length=10, choices=DIFFICULTY_CHOICES, default='easy')
    reward_points = models.IntegerField()
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField()
    participant_count = models.IntegerField(default=0)
    level = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class ChallengeExercise(models.Model):
    challenge = models.ForeignKey(Challenge, related_name='exercises', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    order = models.IntegerField()
    speaking_text_content = models.BinaryField()  # lưu hex
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class UserChallengeProgress(models.Model):
    STATUS_CHOICES = [('not_started', 'Not Started'), ('in_progress', 'In Progress'), ('completed', 'Completed')]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    challenge = models.ForeignKey(Challenge, on_delete=models.CASCADE)
    score = models.IntegerField(default=0)
    completion_percentage = models.FloatField(default=0.0)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='not_started')
    last_attempted_date = models.DateTimeField(auto_now=True)
    completed_date = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ('user', 'challenge')

class UserExerciseAttempt(models.Model):
    user_challenge_progress = models.ForeignKey(UserChallengeProgress, on_delete=models.CASCADE)
    challenge_exercise = models.ForeignKey(ChallengeExercise, on_delete=models.CASCADE)
    user_audio_file_path = models.FileField(upload_to='challenge_audio/', null=True, blank=True)
    transcribed_text = models.TextField()
    score = models.FloatField()
    detailed_feedback = models.JSONField()
    attempted_at = models.DateTimeField(auto_now_add=True)
# Bảng để lưu xếp hạng người dùng
class UserLoginStreak(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    last_login_date = models.DateField(null=True, blank=True)
    streak_count = models.IntegerField(default=0)

class UserWeeklyScore(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    year = models.IntegerField()
    week = models.IntegerField()
    total_score = models.IntegerField(default=0)

    class Meta:
        unique_together = ('user', 'year', 'week')