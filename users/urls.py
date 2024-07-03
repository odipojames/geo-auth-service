from django.urls import path
from users.views import (RegisterUserView, CustomTokenObtainView, ResetPasswordRequestView, 
                         PasswordResetConfirmView, ProfileUpdateView,ProfileListView, ProfileRetrieveView,RegisterAdminView)

urlpatterns = [
    path('register/', RegisterUserView.as_view(), name='register'),
    path('register-admin/', RegisterAdminView.as_view(), name='register-admin'),
    path('login/', CustomTokenObtainView.as_view(), name='token_obtain_pair'),
    path('reset-password/', ResetPasswordRequestView.as_view(), name='reset_password_request'),
    path('confirm-reset-password/', PasswordResetConfirmView.as_view(), name='confirm_reset_password'),
    path('profile/', ProfileUpdateView.as_view(), name='profile-update'),
    path('profiles/', ProfileListView.as_view(), name='profile-list'),
    path('profiles/<uuid:pk>', ProfileRetrieveView.as_view(), name='profile-detail'),
]
