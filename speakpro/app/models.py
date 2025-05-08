from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.utils import timezone

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
        on_delete=models.CASCADE, 
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
# Bảng cho chức năng Challenge
class ChallengeCategory(models.Model):
    """
    Phân loại các Challenge (VD: Daily, Weekly, Monthly).
    """
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    # Thêm trường slug nếu cần URL thân thiện
    # slug = models.SlugField(max_length=120, unique=True, blank=True)

    class Meta:
        verbose_name = "Challenge Category"
        verbose_name_plural = "Challenge Categories"
        ordering = ['name']

    def __str__(self):
        return self.name

class Challenge(models.Model):
    """
    Định nghĩa một Challenge.
    """
    title = models.CharField(max_length=255)
    description = models.TextField()
    category = models.ForeignKey(ChallengeCategory, on_delete=models.SET_NULL, null=True, related_name='challenges')
    level = models.ForeignKey(Level, on_delete=models.SET_NULL, null=True, related_name='challenges') # Tái sử dụng model Level
    points_reward = models.PositiveIntegerField(default=100, help_text="Points awarded for completing the entire challenge")
    start_date = models.DateTimeField(null=True, blank=True, help_text="When the challenge becomes available (optional)")
    end_date = models.DateTimeField(null=True, blank=True, help_text="When the challenge ends (optional)")
    duration_days = models.PositiveIntegerField(null=True, blank=True, help_text="Alternative to end_date, duration in days from start_date or creation")
    is_featured = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True, help_text="Manually activate/deactivate. Can also be computed.")
    # image = models.ImageField(upload_to='challenge_images/', null=True, blank=True) # Nếu cần ảnh cho challenge

    class Meta:
        ordering = ['-start_date', 'title']
        verbose_name = "Challenge"
        verbose_name_plural = "Challenges"

    def __str__(self):
        return self.title

    @property
    def get_is_currently_active(self):
        """Kiểm tra xem challenge có đang active dựa trên ngày tháng không."""
        if not self.is_active: # Nếu bị tắt thủ công
            return False
        now = timezone.now()
        if self.start_date and now < self.start_date:
            return False
        if self.end_date and now > self.end_date:
            return False
        # Nếu có duration_days và không có end_date cụ thể
        if self.duration_days and not self.end_date:
            effective_start_date = self.start_date if self.start_date else self.date_created # Giả sử có date_created
            if now > (effective_start_date + timezone.timedelta(days=self.duration_days)):
                return False
        return True


class ChallengeExercise(models.Model):
    """
    Một bài tập cụ thể trong một Challenge.
    Mỗi bài tập sẽ liên kết đến một SpeakingText.
    """
    challenge = models.ForeignKey(Challenge, on_delete=models.CASCADE, related_name='exercises')
    speaking_text = models.ForeignKey(SpeakingText, on_delete=models.CASCADE, related_name='challenge_exercises') # Tái sử dụng SpeakingText
    order = models.PositiveIntegerField(default=0, help_text="Order of this exercise within the challenge")
    # points_value = models.PositiveIntegerField(default=0, help_text="Points for completing this specific exercise (if any)") # Có thể không cần nếu chỉ tính điểm tổng challenge

    class Meta:
        ordering = ['challenge', 'order']
        unique_together = ('challenge', 'speaking_text', 'order') # Đảm bảo thứ tự và bài tập là duy nhất trong challenge
        verbose_name = "Challenge Exercise"
        verbose_name_plural = "Challenge Exercises"

    def __str__(self):
        return f"{self.challenge.title} - Ex{self.order}: {self.speaking_text.title}"


class UserChallengeAttempt(models.Model):
    """
    Lưu lại nỗ lực của người dùng khi tham gia một Challenge.
    """
    STATUS_CHOICES = [
        ('not_started', 'Not Started'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        # ('failed', 'Failed'), # Nếu có trạng thái thất bại
    ]
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='challenge_attempts')
    challenge = models.ForeignKey(Challenge, on_delete=models.CASCADE, related_name='attempts_by_users')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='not_started')
    points_earned = models.PositiveIntegerField(default=0)
    started_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-started_at']
        unique_together = ('user', 'challenge') # Mỗi user chỉ có một attempt chính cho một challenge
        verbose_name = "User Challenge Attempt"
        verbose_name_plural = "User Challenge Attempts"

    def __str__(self):
        return f"{self.user.username}'s attempt on {self.challenge.title} ({self.status})"

    def update_progress_and_points(self):
        """
        Cập nhật tiến độ và điểm dựa trên các UserChallengeExerciseAttempt.
        Gọi hàm này sau khi một exercise được hoàn thành.
        """
        completed_exercises_count = self.exercise_attempts.filter(is_completed=True).count()
        total_exercises_count = self.challenge.exercises.count()

        # Cập nhật điểm (ví dụ đơn giản: mỗi exercise hoàn thành được 10 điểm, cộng với điểm thưởng challenge)
        # Hoặc nếu challenge chỉ có điểm thưởng khi hoàn thành toàn bộ:
        # current_points = 0
        # for ex_attempt in self.exercise_attempts.filter(is_completed=True):
        #     if ex_attempt.user_practice_log and ex_attempt.user_practice_log.score:
        #          # Giả sử điểm của exercise là điểm từ practice_log (chia cho 10 chẳng hạn)
        #          current_points += (ex_attempt.user_practice_log.score / 10) # Ví dụ

        # Tạm thời, ta sẽ tính điểm dựa trên điểm thưởng của challenge khi hoàn thành
        # Điểm chi tiết hơn có thể được thêm sau

        if total_exercises_count > 0 and completed_exercises_count >= total_exercises_count:
            if self.status != 'completed': # Chỉ cập nhật 1 lần khi hoàn thành
                self.status = 'completed'
                self.completed_at = timezone.now()
                self.points_earned = self.challenge.points_reward # Gán điểm thưởng của challenge
                # TODO: Gọi hàm cập nhật streak và achievements ở đây
                # self.user.update_challenge_streak(self.challenge)
                # self.user.check_and_award_achievements_for_challenge_completion(self.challenge)
        elif completed_exercises_count > 0:
            self.status = 'in_progress'
        
        self.save()
        return {"completed_exercises": completed_exercises_count, "total_exercises": total_exercises_count}


class UserChallengeExerciseAttempt(models.Model):
    """
    Lưu lại nỗ lực của người dùng với một bài tập cụ thể trong một Challenge Attempt.
    """
    user_challenge_attempt = models.ForeignKey(UserChallengeAttempt, on_delete=models.CASCADE, related_name='exercise_attempts')
    challenge_exercise = models.ForeignKey(ChallengeExercise, on_delete=models.CASCADE, related_name='attempts_by_users')
    # Liên kết với UserPracticeLog để lưu điểm, chi tiết nhận dạng giọng nói,...
    user_practice_log = models.OneToOneField(UserPracticeLog, on_delete=models.SET_NULL, null=True, blank=True, related_name='challenge_exercise_attempt')
    is_completed = models.BooleanField(default=False)
    score_at_completion = models.FloatField(null=True, blank=True, help_text="Score from UserPracticeLog at the time of completion")
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['challenge_exercise__order']
        unique_together = ('user_challenge_attempt', 'challenge_exercise')
        verbose_name = "User Challenge Exercise Attempt"
        verbose_name_plural = "User Challenge Exercise Attempts"

    def __str__(self):
        return f"Attempt by {self.user_challenge_attempt.user.username} on Ex: {self.challenge_exercise.speaking_text.title} (Completed: {self.is_completed})"


class UserChallengeStreak(models.Model):
    """
    Theo dõi chuỗi ngày hoàn thành challenge liên tiếp của người dùng.
    """
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, primary_key=True, related_name='challenge_streak')
    current_streak_days = models.PositiveIntegerField(default=0)
    longest_streak_days = models.PositiveIntegerField(default=0)
    last_challenge_completed_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.username}'s streak: {self.current_streak_days} days"

    def update_streak(self, completion_date_obj):
        """
        Cập nhật streak khi user hoàn thành một challenge.
        completion_date_obj là một đối tượng date (không phải datetime).
        """
        today = completion_date_obj

        if self.last_challenge_completed_date:
            delta = today - self.last_challenge_completed_date
            if delta.days == 1: # Hoàn thành vào ngày kế tiếp
                self.current_streak_days += 1
            elif delta.days > 1: # Bỏ lỡ ngày, reset streak
                self.current_streak_days = 1
            # Nếu delta.days == 0, tức là hoàn thành nhiều challenge trong cùng 1 ngày, không tăng streak.
        else: # Lần đầu hoàn thành challenge
            self.current_streak_days = 1

        if self.current_streak_days > self.longest_streak_days:
            self.longest_streak_days = self.current_streak_days
        
        self.last_challenge_completed_date = today
        self.save()
        # TODO: Kiểm tra achievement liên quan đến streak ở đây
        # self.user.check_and_award_streak_achievements()

class Achievement(models.Model):
    """
    Định nghĩa các loại thành tựu người dùng có thể đạt được.
    """
    ACHIEVEMENT_TYPE_CHOICES = [
        ('streak', 'Streak Based'),
        ('challenge_completion', 'Challenge Completion Based'),
        ('points_earned', 'Points Earned Based'),
        ('other', 'Other'),
    ]
    name = models.CharField(max_length=150, unique=True)
    description = models.TextField()
    icon_url = models.CharField(max_length=255, blank=True, null=True, help_text="URL or path to an icon image")
    achievement_type = models.CharField(max_length=30, choices=ACHIEVEMENT_TYPE_CHOICES, default='other')
    # criteria: JSONField lưu các điều kiện, ví dụ:
    # cho streak: {"days": 5}
    # cho challenge_completion: {"challenge_id": 1} hoặc {"category_id": 2, "count": 3}
    # cho points_earned: {"total_challenge_points": 1000}
    criteria = models.JSONField(default=dict, help_text="JSON criteria to unlock this achievement")
    points_reward = models.PositiveIntegerField(default=0, help_text="Points awarded when achieving this")

    class Meta:
        ordering = ['name']
        verbose_name = "Achievement"
        verbose_name_plural = "Achievements"

    def __str__(self):
        return self.name

class UserAchievement(models.Model):
    """
    Ghi lại thành tựu mà người dùng đã đạt được.
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='achievements')
    achievement = models.ForeignKey(Achievement, on_delete=models.CASCADE, related_name='earned_by_users')
    achieved_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-achieved_at']
        unique_together = ('user', 'achievement') # User chỉ nhận mỗi achievement một lần
        verbose_name = "User Achievement"
        verbose_name_plural = "User Achievements"

    def __str__(self):
        return f"{self.user.username} earned {self.achievement.name}"
