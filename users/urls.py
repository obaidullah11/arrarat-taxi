from django.urls import path
# from .views import DriverListAPIView
from users.views import SendPasswordResetEmailView,DriverListAPIView, UserChangePasswordView, UserLoginView, UserProfileView, UserRegistrationView, UserPasswordResetView,set_user_deleted
urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('changepassword/', UserChangePasswordView.as_view(), name='changepassword'),
    path('send-reset-password-email/', SendPasswordResetEmailView.as_view(), name='send-reset-password-email'),
    path('reset-password/<uid>/<token>/', UserPasswordResetView.as_view(), name='reset-password'),
    path('drivers/', DriverListAPIView.as_view(), name='driver_list'),
    path('users/<int:user_id>/set_deleted/',set_user_deleted, name='set_user_deleted'),
]