# accounts/serializers.py
from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from django.core.validators import EmailValidator
from django.utils import timezone
from .models import User, UserProfile, PasswordResetOTP
import random
import string

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('theme_preference', 'language_preference', 'email_notifications', 
                 'favorite_languages', 'coding_experience', 'linkedin_url', 'portfolio_url')

class UserSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer(required=False)
    
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'user_type',
                 'phone_number', 'college_name', 'year_of_study', 'branch',
                 'bio', 'profile_picture', 'github_username', 'total_code_reviews',
                 'total_bugs_found', 'average_quality_score', 'profile')
        read_only_fields = ('id', 'total_code_reviews', 'total_bugs_found', 
                           'average_quality_score', 'user_type')

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[validate_password])
    confirm_password = serializers.CharField(write_only=True)
    email = serializers.EmailField(validators=[EmailValidator()])
    
    class Meta:
        model = User
        fields = (
            'username', 'email', 'password', 'confirm_password', 
            'first_name', 'last_name', 'phone_number', 
            'college_name', 'year_of_study', 'branch', 
            'company_name', 'job_title', 'years_of_experience', 'skills',
            'user_type'
        )
    
    def validate(self, data):
        # Check if passwords match
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError({
                'confirm_password': 'Passwords do not match.'
            })
        
        # Check if username is taken
        if User.objects.filter(username=data['username']).exists():
            raise serializers.ValidationError({
                'username': 'This username is already taken.'
            })
        
        # Check if email is taken
        if User.objects.filter(email=data['email']).exists():
            raise serializers.ValidationError({
                'email': 'This email is already registered.'
            })
        
        return data
    
    def create(self, validated_data):
        validated_data.pop('confirm_password')
        user = User.objects.create_user(**validated_data)
        return user

class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)
    
    def validate(self, data):
        username = data.get('username')
        password = data.get('password')
        
        print(f"🔐 Validating login for: {username}")
        
        # Check if user exists
        try:
            user = User.objects.get(username=username)
            print(f"✅ User found: {user.username}")
        except User.DoesNotExist:
            print(f"❌ User not found: {username}")
            raise serializers.ValidationError('Invalid username or password.')
        
        # Try authentication with the user object
        if user.check_password(password):
            print(f"✅ Password correct for: {user.username}")
            data['user'] = user
            return data
        else:
            print(f"❌ Password incorrect for: {user.username}")
            raise serializers.ValidationError('Invalid username or password.')
        
        # Alternative: use authenticate
        # user = authenticate(username=username, password=password)
        # if not user:
        #     raise serializers.ValidationError('Invalid username or password.')
        
        # if not user.is_active:
        #     raise serializers.ValidationError('This account is deactivated.')
        
        # data['user'] = user
        # return data

class PasswordChangeSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True, validators=[validate_password])
    confirm_new_password = serializers.CharField(required=True)
    
    def validate(self, data):
        if data['new_password'] != data['confirm_new_password']:
            raise serializers.ValidationError({
                'confirm_new_password': 'Passwords do not match.'
            })
        return data

class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    
    def validate_email(self, value):
        if not User.objects.filter(email=value).exists():
            raise serializers.ValidationError('No user found with this email address.')
        return value

class PasswordResetVerifySerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    otp = serializers.CharField(required=True, max_length=6)
    
    def validate(self, data):
        try:
            user = User.objects.get(email=data['email'])
            otp_obj = PasswordResetOTP.objects.filter(
                user=user,
                otp=data['otp'],
                is_used=False,
                expires_at__gte=timezone.now()
            ).first()
            
            if not otp_obj:
                raise serializers.ValidationError({
                    'otp': 'Invalid or expired OTP.'
                })
            
            data['user'] = user
            return data
        except User.DoesNotExist:
            raise serializers.ValidationError({
                'email': 'No user found with this email address.'
            })

class PasswordResetConfirmSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    otp = serializers.CharField(required=True, max_length=6)
    new_password = serializers.CharField(required=True, validators=[validate_password])
    confirm_new_password = serializers.CharField(required=True)
    
    def validate(self, data):
        if data['new_password'] != data['confirm_new_password']:
            raise serializers.ValidationError({
                'confirm_new_password': 'Passwords do not match.'
            })
        
        try:
            user = User.objects.get(email=data['email'])
            otp_obj = PasswordResetOTP.objects.filter(
                user=user,
                otp=data['otp'],
                is_used=False,
                expires_at__gte=timezone.now()
            ).first()
            
            if not otp_obj:
                raise serializers.ValidationError({
                    'otp': 'Invalid or expired OTP.'
                })
            
            data['user'] = user
            data['otp_obj'] = otp_obj
            return data
        except User.DoesNotExist:
            raise serializers.ValidationError({
                'email': 'No user found with this email address.'
            })