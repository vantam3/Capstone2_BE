from django.urls import path
from .views import home, RegisterView, LoginView, LogoutView, ForgotPasswordView, ResetPasswordView  # Import các view từ file views.py

urlpatterns = [
    path('', home, name='home'),  # Route cho hàm home
    path('register/', RegisterView.as_view(), name='register'),  # Route cho đăng ký
    path('login/', LoginView.as_view(), name='login'),  # Route cho đăng nhập
    path('logout/', LogoutView.as_view(), name='logout'),  # Route cho đăng xuất
    path('forgot-password/', ForgotPasswordView.as_view(), name='forgot_password'),  # Route cho quên mật khẩu
    path('reset-password/', ResetPasswordView.as_view(), name='reset_password'),  # Route cho đặt lại mật khẩu
]