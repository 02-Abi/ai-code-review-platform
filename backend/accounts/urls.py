from django.urls import path
from . import views

urlpatterns = [
    # Authentication
    path('register/', views.UserRegistrationView.as_view(), name='register'),
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('logout/', views.UserLogoutView.as_view(), name='logout'),
    
    # Profile
    path('profile/', views.UserProfileView.as_view(), name='profile'),
    path('profile/update/', views.UserProfileView.as_view(), name='profile_update'),
    
    # Password
    path('password/change/', views.PasswordChangeView.as_view(), name='password_change'),
    path('password/reset/request/', views.PasswordResetRequestView.as_view(), name='password_reset_request'),
    path('password/reset/verify/', views.PasswordResetVerifyView.as_view(), name='password_reset_verify'),
    path('password/reset/confirm/', views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    
    # Statistics
    path('statistics/', views.UserStatisticsView.as_view(), name='user_statistics'),
    
    # Admin
    path('all-users/', views.AllUsersView.as_view(), name='all_users'),
]