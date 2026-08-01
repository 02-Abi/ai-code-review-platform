from rest_framework import status, generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate, update_session_auth_hash
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings
from .models import User, PasswordResetOTP
from .serializers import (
    UserSerializer, UserRegistrationSerializer, UserLoginSerializer,
    PasswordChangeSerializer, PasswordResetRequestSerializer,
    PasswordResetVerifySerializer, PasswordResetConfirmSerializer,
    UserProfileSerializer
)
import random
import logging

logger = logging.getLogger(__name__)

class UserRegistrationView(APIView):
    """
    User registration endpoint
    """
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            
            # Generate tokens
            refresh = RefreshToken.for_user(user)
            
            return Response({
                'status': 'success',
                'message': 'User registered successfully.',
                'user': UserSerializer(user).data,
                'tokens': {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                }
            }, status=status.HTTP_201_CREATED)
        
        # Log errors for debugging
        print("Registration errors:", serializer.errors)
        
        return Response({
            'status': 'error',
            'message': 'Registration failed.',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

class UserLoginView(APIView):
    """
    User login endpoint
    """
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            
            # Update last login
            user.last_login = timezone.now()
            user.save(update_fields=['last_login'])
            
            # Generate tokens
            refresh = RefreshToken.for_user(user)
            
            return Response({
                'status': 'success',
                'message': 'Login successful.',
                'user': UserSerializer(user).data,
                'tokens': {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                }
            }, status=status.HTTP_200_OK)
        
        return Response({
            'status': 'error',
            'message': 'Login failed.',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

class UserLogoutView(APIView):
    """
    User logout endpoint - blacklists refresh token
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        try:
            refresh_token = request.data.get('refresh')
            if refresh_token:
                token = RefreshToken(refresh_token)
                token.blacklist()
                
            return Response({
                'status': 'success',
                'message': 'Logout successful.'
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                'status': 'error',
                'message': 'Logout failed.',
                'detail': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)

class UserProfileView(generics.RetrieveUpdateAPIView):
    """
    Get and update user profile
    """
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_object(self):
        return self.request.user
    
    def update(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = self.get_serializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'status': 'success',
                'message': 'Profile updated successfully.',
                'user': serializer.data
            }, status=status.HTTP_200_OK)
        
        return Response({
            'status': 'error',
            'message': 'Profile update failed.',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

class PasswordChangeView(APIView):
    """
    Change user password
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        serializer = PasswordChangeSerializer(data=request.data)
        if serializer.is_valid():
            user = request.user
            
            # Check old password
            if not user.check_password(serializer.validated_data['old_password']):
                return Response({
                    'status': 'error',
                    'message': 'Current password is incorrect.',
                    'errors': {'old_password': 'Current password is incorrect.'}
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # Set new password
            user.set_password(serializer.validated_data['new_password'])
            user.save()
            update_session_auth_hash(request, user)
            
            return Response({
                'status': 'success',
                'message': 'Password changed successfully.'
            }, status=status.HTTP_200_OK)
        
        return Response({
            'status': 'error',
            'message': 'Password change failed.',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

class PasswordResetRequestView(APIView):
    """
    Request password reset OTP
    """
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        serializer = PasswordResetRequestSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            user = User.objects.get(email=email)
            
            # Generate OTP
            otp = ''.join(random.choices('0123456789', k=6))
            
            # Delete existing OTPs
            PasswordResetOTP.objects.filter(user=user, is_used=False).delete()
            
            # Create new OTP
            otp_obj = PasswordResetOTP.objects.create(
                user=user,
                otp=otp,
                expires_at=timezone.now() + timezone.timedelta(minutes=10)
            )
            
            # Send email (in production, use proper email templates)
            try:
                send_mail(
                    subject='Password Reset OTP',
                    message=f'Your OTP for password reset is: {otp}\n\nThis OTP is valid for 10 minutes.',
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[email],
                    fail_silently=False,
                )
            except Exception as e:
                logger.error(f"Failed to send password reset email: {str(e)}")
                return Response({
                    'status': 'error',
                    'message': 'Failed to send OTP email. Please try again later.'
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
            return Response({
                'status': 'success',
                'message': 'OTP sent to your email address.',
                'email': email
            }, status=status.HTTP_200_OK)
        
        return Response({
            'status': 'error',
            'message': 'Password reset request failed.',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

class PasswordResetVerifyView(APIView):
    """
    Verify password reset OTP
    """
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        serializer = PasswordResetVerifySerializer(data=request.data)
        if serializer.is_valid():
            return Response({
                'status': 'success',
                'message': 'OTP verified successfully.',
                'email': serializer.validated_data['email']
            }, status=status.HTTP_200_OK)
        
        return Response({
            'status': 'error',
            'message': 'OTP verification failed.',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

class PasswordResetConfirmView(APIView):
    """
    Confirm password reset with OTP
    """
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        serializer = PasswordResetConfirmSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            otp_obj = serializer.validated_data['otp_obj']
            
            # Set new password
            user.set_password(serializer.validated_data['new_password'])
            user.save()
            
            # Mark OTP as used
            otp_obj.is_used = True
            otp_obj.save()
            
            return Response({
                'status': 'success',
                'message': 'Password reset successfully.'
            }, status=status.HTTP_200_OK)
        
        return Response({
            'status': 'error',
            'message': 'Password reset failed.',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

class UserStatisticsView(APIView):
    """
    Get user statistics
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        user = request.user
        
        return Response({
            'username': user.username,
            'total_code_reviews': user.total_code_reviews,
            'total_bugs_found': user.total_bugs_found,
            'average_quality_score': round(user.average_quality_score, 2),
            'user_type': user.user_type,
            'is_verified': user.is_verified,
            'member_since': user.date_joined.strftime('%B %d, %Y')
        }, status=status.HTTP_200_OK)

class AllUsersView(generics.ListAPIView):
    """
    Admin view to list all users
    """
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]
    
    def get_queryset(self):
        return User.objects.all().order_by('-created_at')