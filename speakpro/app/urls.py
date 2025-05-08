from django.urls import path
from .views import home, RegisterView, LoginView, LogoutView, ForgotPasswordView, ResetPasswordView, SpeakingTextSearchView, UserPracticeLogView, DashboardStatsView
from .views import  GenreListView, GenreDetailView, SpeakingTextListView, SpeakingTextDetailView, AudioListView, AudioDetailView,UserListView
from django.conf import settings
from django.conf.urls.static import static
from .views import home
from . import views

urlpatterns = [
    path('', home, name='home'),  # Route cho hàm home
    path('register/', RegisterView.as_view(), name='register'),  # Route cho đăng ký
    path('login/', LoginView.as_view(), name='login'),  # Route cho đăng nhập
    path('logout/', LogoutView.as_view(), name='logout'),  # Route cho đăng xuất
    path('forgot-password/', ForgotPasswordView.as_view(), name='forgot_password'),  # Route cho quên mật khẩu
    path('reset-password/', ResetPasswordView.as_view(), name='reset_password'),  # Route cho đặt lại mật khẩu
    # tìm kiếm SpeakingText Topics
    path('speaking-texts/search/', SpeakingTextSearchView.as_view(), name='speaking-text-search'),
    # User Progress & History URL
    path('practice-logs/', UserPracticeLogView.as_view(), name='user-practice-log-list-create'),
    # --- Dashboard Stats URL ---
    path('dashboard/stats/', DashboardStatsView.as_view(), name='dashboard-stats'),
    # Challenge Categories
    path('api/challenge-categories/', 
         views.ChallengeCategoryViewSet.as_view({'get': 'list'}), 
         name='challenge-category-list'),
    path('api/challenge-categories/<int:pk>/', 
         views.ChallengeCategoryViewSet.as_view({'get': 'retrieve'}), 
         name='challenge-category-detail'),

    # Challenges
    path('api/challenges/', 
         views.ChallengeViewSet.as_view({'get': 'list'}), 
         name='challenge-list'),
    path('api/challenges/<int:pk>/', 
         views.ChallengeViewSet.as_view({'get': 'retrieve'}), 
         name='challenge-detail'),
    
    # Custom actions cho ChallengeViewSet
    path('api/challenges/<int:pk>/start/', 
         views.ChallengeViewSet.as_view({'post': 'start_challenge'}), 
         name='challenge-start'),
    path('api/challenges/<int:pk>/exercises/',
         views.ChallengeViewSet.as_view({'get': 'list_exercises_with_status'}),
         name='challenge-list-exercises-with-status'),
    path('api/challenges/<int:pk>/leaderboard/', 
         views.ChallengeViewSet.as_view({'get': 'leaderboard'}), 
         name='challenge-leaderboard'),

    #Submit Challenge Exercise Attempt
    path('api/challenges/<int:challenge_pk>/exercises/<int:exercise_pk>/submit-attempt/', 
         views.ChallengeExerciseSubmitAttemptView.as_view(), 
         name='challenge-exercise-submit-attempt'),
    # Leadersboard     
    path('api/global-leaderboard/', 
         views.GlobalLeaderboardView.as_view(), 
         name='global-leaderboard'),

    # User Challenge Data & Achievements 
    path('api/user-challenge-data/', 
         views.UserChallengeDataView.as_view(), 
         name='user-challenge-data'),
    # Thể loại
    path('genres/', GenreListView.as_view(), name='genre-list'),
    path('genres/<int:pk>/', GenreDetailView.as_view(), name='genre-detail'),
    # Đoạn văn mẫu
    path('', home, name='home'),
    path('users/', UserListView.as_view(), name='user-list'),  

    # GENRES
    path('genres/', GenreListView.as_view(), name='genre-list'),
    path('genres/<int:pk>/', GenreDetailView.as_view(), name='genre-detail'),

    # TEXT
    path('speaking-texts/', SpeakingTextListView.as_view(), name='speaking-text-list'),
    path('speaking-texts/<int:pk>/', SpeakingTextDetailView.as_view(), name='speaking-text-detail'),

    #AUDIO
    path('audios/', AudioListView.as_view(), name='audio-list'),
    path('audios/<int:pk>/', AudioDetailView.as_view(), name='audio-detail'),
    # path('api/speech-to-text/', SpeechToTextAPIView.as_view(), name='speech_to_text'),
    
    #CRUD text
    path('api/add/', views.SpeakingTextCreateAPIView.as_view(), name='add_speaking_text'),
    path('api/update/<int:id>/', views.SpeakingTextUpdateAPIView.as_view(), name='edit_speaking_text'),
    path('api/delete/<int:id>/', views.SpeakingTextDeleteAPIView.as_view(), name='delete_speaking_text'),
    
    #user
    path('api/users/create/', views.UserCreateAPIView.as_view(), name='create-user'),
    path('api/users/update/<int:id>/', views.UserUpdateAPIView.as_view(), name='update-user'),
    path('api/users/delete/<int:id>/', views.UserDeleteAPIView.as_view(), name='delete-user'),

    path('levels/', views.LevelListAPIView.as_view(), name='list-levels'),
    path('speaking-texts/filter/', views.SpeakingTextFilterAPIView.as_view(), name='filter-speaking-texts'),
    path('upload-user-audio/', views.upload_user_audio, name='upload_user_audio'),

    path('api/submit-speaking/', views.SubmitSpeakingAPIView.as_view(), name='submit-speaking'),
    
    #ai
    path('api/dialogue/', views.DialogueAPIView.as_view(), name='ai-dialogue'),
    

]    + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    









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
