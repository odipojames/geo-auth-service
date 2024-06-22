from django.urls import path
from users.views import (RegisterUserView, CustomTokenObtainView, ResetPasswordRequestView, 
                         PasswordResetConfirmView, ProfileUpdateView,ProfileListView, ProfileRetrieveView)

urlpatterns = [
    path('api/register/', RegisterUserView.as_view(), name='register'),
    path('api/login/', CustomTokenObtainView.as_view(), name='token_obtain_pair'),
    path('api/reset-password/', ResetPasswordRequestView.as_view(), name='reset_password_request'),
    path('api/confirm-reset-password/', PasswordResetConfirmView.as_view(), name='confirm_reset_password'),
    path('api/profile/', ProfileUpdateView.as_view(), name='profile-update'),
    path('api/profiles/', ProfileListView.as_view(), name='profile-list'),
    path('api/profiles/<int:pk>/', ProfileRetrieveView.as_view(), name='profile-detail'),
]
