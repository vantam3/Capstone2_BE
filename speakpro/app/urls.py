from django.urls import path
from .views import GenreListView, GenreDetailView, SpeakingTextListView, SpeakingTextDetailView, AudioListView, AudioDetailView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Thể loại
    path('genres/', GenreListView.as_view(), name='genre-list'),
    path('genres/<int:pk>/', GenreDetailView.as_view(), name='genre-detail'),

    # Đoạn văn mẫu
    path('speaking-texts/', SpeakingTextListView.as_view(), name='speaking-text-list'),
    path('speaking-texts/<int:pk>/', SpeakingTextDetailView.as_view(), name='speaking-text-detail'),

    # Âm thanh
    path('audios/', AudioListView.as_view(), name='audio-list'),
    path('audios/<int:pk>/', AudioDetailView.as_view(), name='audio-detail'),
]
# Cung cấp các tệp media trong môi trường phát triển
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    

# from app.models import Audio, SpeakingText

# # Danh sách các id của SpeakingText và các tệp MP3 tương ứng
# speaking_texts_and_files = [
#     (1, ['audio_files/1.mp3']),  # SpeakingText id = 1
#     (2, ['audio_files/2.mp3']),  # SpeakingText id = 2
#     (3, ['audio_files/3.mp3']),
#     (4, ['audio_files/4.mp3']), 
#     (5, ['audio_files/5.mp3']),
#     (6, ['audio_files/6.mp3']), 
#     (7, ['audio_files/7.mp3']), 
#     (8, ['audio_files/8.mp3']), 
#     (9, ['audio_files/9.mp3']), 
#     (10, ['audio_files/10.mp3']), 
#     (11, ['audio_files/11.mp3']), 
#     (12, ['audio_files/12.mp3']),  # SpeakingText id = 12
# ]

# # Lặp qua các đối tượng SpeakingText và danh sách tệp MP3
# for speaking_text_id, audio_files in speaking_texts_and_files:
#     # Lấy đối tượng SpeakingText từ cơ sở dữ liệu
#     speaking_text = SpeakingText.objects.get(id=speaking_text_id)
    
#     # Lặp qua danh sách các tệp MP3 cho mỗi SpeakingText
#     for audio_file_path in audio_files:
#         # Tạo đối tượng Audio và lưu vào cơ sở dữ liệu
#         audio = Audio.objects.create(
#             speaking_text=speaking_text,  # Liên kết đối tượng SpeakingText
#             audio_file=audio_file_path  # Lưu đường dẫn tệp MP3 vào cơ sở dữ liệu
#         )

