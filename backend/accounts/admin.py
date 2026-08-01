from django.contrib import admin

# Register your models here.
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, UserProfile, PasswordResetOTP

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'user_type', 'is_active', 'total_code_reviews')
    list_filter = ('user_type', 'is_active', 'is_verified')
    search_fields = ('username', 'email', 'phone_number')
    
    fieldsets = UserAdmin.fieldsets + (
        ('User Information', {
            'fields': ('user_type', 'phone_number', 'college_name', 'year_of_study', 
                      'branch', 'bio', 'profile_picture')
        }),
        ('Statistics', {
            'fields': ('total_code_reviews', 'total_bugs_found', 'average_quality_score')
        }),
        ('GitHub', {
            'fields': ('github_username', 'github_access_token')
        }),
    )
    
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('User Information', {
            'fields': ('user_type', 'phone_number', 'college_name')
        }),
    )

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'theme_preference', 'email_notifications')
    search_fields = ('user__username', 'user__email')

@admin.register(PasswordResetOTP)
class PasswordResetOTPAdmin(admin.ModelAdmin):
    list_display = ('user', 'otp', 'created_at', 'expires_at', 'is_used')
    list_filter = ('is_used',)