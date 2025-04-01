from django.db import models

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
