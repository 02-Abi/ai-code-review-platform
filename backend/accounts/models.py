from django.db import models

# Create your models here.
"""
Custom User Model for AI Code Review Platform
"""
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from django.utils import timezone
from django.core.validators import MinLengthValidator, MaxLengthValidator
import uuid

class User(AbstractUser):
    """
    Custom User model with additional fields
    """
    # Override groups and user_permissions to avoid conflicts
    groups = models.ManyToManyField(
        Group,
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to.',
        related_name='custom_user_set',
        related_query_name='user',
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name='custom_user_set',
        related_query_name='user',
    )
    company_name = models.CharField(max_length=200, blank=True, null=True)
    job_title = models.CharField(max_length=100, blank=True, null=True)
    years_of_experience = models.IntegerField(blank=True, null=True)
    skills = models.TextField(blank=True, null=True)
    # User Types
    USER_TYPES = (
        ('student', 'Student'),
        ('admin', 'Admin'),
    )
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_type = models.CharField(max_length=20, choices=USER_TYPES, default='student')
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    college_name = models.CharField(max_length=200, blank=True, null=True)
    year_of_study = models.IntegerField(blank=True, null=True)
    branch = models.CharField(max_length=100, blank=True, null=True)
    
    # Profile
    profile_picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True)
    bio = models.TextField(max_length=500, blank=True)
    
    # GitHub Integration
    github_username = models.CharField(max_length=100, blank=True, null=True)
    github_access_token = models.CharField(max_length=500, blank=True, null=True)
    
    # Statistics
    total_code_reviews = models.IntegerField(default=0)
    total_bugs_found = models.IntegerField(default=0)
    average_quality_score = models.FloatField(default=0.0)
    
    # Timestamps
    last_login = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    is_verified = models.BooleanField(default=False)
    
    class Meta:
        db_table = 'users'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['email']),
            models.Index(fields=['username']),
            models.Index(fields=['user_type']),
        ]
    
    def __str__(self):
        return f"{self.username} ({self.user_type})"
    
    def get_full_name(self):
        if self.first_name or self.last_name:
            return f"{self.first_name} {self.last_name}".strip()
        return self.username
    
    def increment_review_count(self):
        self.total_code_reviews += 1
        self.save(update_fields=['total_code_reviews'])
    
    def update_quality_score(self, new_score):
        if self.total_code_reviews > 0:
            total = (self.average_quality_score * (self.total_code_reviews - 1)) + new_score
            self.average_quality_score = total / self.total_code_reviews
        else:
            self.average_quality_score = new_score
        self.save(update_fields=['average_quality_score'])

class UserProfile(models.Model):
    """
    Extended user profile model
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    
    # Preferences
    theme_preference = models.CharField(max_length=20, default='light')
    language_preference = models.CharField(max_length=10, default='en')
    email_notifications = models.BooleanField(default=True)
    
    # Coding preferences
    favorite_languages = models.JSONField(default=list)
    coding_experience = models.CharField(max_length=50, blank=True, null=True)
    
    # Social links
    linkedin_url = models.URLField(blank=True, null=True)
    portfolio_url = models.URLField(blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'user_profiles'
    
    def __str__(self):
        return f"Profile for {self.user.username}"

class PasswordResetOTP(models.Model):
    """
    OTP for password reset
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    otp = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    is_used = models.BooleanField(default=False)
    
    class Meta:
        db_table = 'password_reset_otps'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"OTP for {self.user.username} - {self.otp}"
    
    def is_valid(self):
        return not self.is_used and timezone.now() <= self.expires_at