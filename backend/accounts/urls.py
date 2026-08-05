# accounts/urls.py
from django.urls import path
from . import views

urlpatterns = [
    # Authentication
    path('register/', views.UserRegistrationView.as_view(), name='register'),
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('logout/', views.UserLogoutView.as_view(), name='logout'),
    path('refresh/', views.TokenRefreshView.as_view(), name='token-refresh'),
    path('status/', views.AuthStatusView.as_view(), name='auth-status'),
    
    # Profile
    path('profile/', views.UserProfileView.as_view(), name='profile'),
    
    # Password
    path('password/change/', views.PasswordChangeView.as_view(), name='password-change'),
    path('password/reset/', views.PasswordResetRequestView.as_view(), name='password-reset'),
    path('password/reset/verify/', views.PasswordResetVerifyView.as_view(), name='password-reset-verify'),
    path('password/reset/confirm/', views.PasswordResetConfirmView.as_view(), name='password-reset-confirm'),
    
    # Statistics
    path('statistics/', views.UserStatisticsView.as_view(), name='statistics'),
    
    # Admin
    path('all/', views.AllUsersView.as_view(), name='all-users'),
]