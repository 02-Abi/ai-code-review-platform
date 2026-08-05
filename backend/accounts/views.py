# accounts/views.py
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


# ============================================================
# TOKEN REFRESH VIEW
# ============================================================

class TokenRefreshView(APIView):
    """
    Refresh access token using refresh token
    """
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        refresh_token = request.data.get('refresh')
        if not refresh_token:
            return Response({
                'status': 'error',
                'message': 'Refresh token is required'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            refresh = RefreshToken(refresh_token)
            return Response({
                'status': 'success',
                'access': str(refresh.access_token)
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                'status': 'error',
                'message': 'Invalid or expired refresh token',
                'detail': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)


# ============================================================
# USER REGISTRATION VIEW
# ============================================================

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
        
        print("Registration errors:", serializer.errors)
        
        return Response({
            'status': 'error',
            'message': 'Registration failed.',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


# ============================================================
# USER LOGIN VIEW
# ============================================================

# accounts/views.py - Updated UserLoginView with more debugging

class UserLoginView(APIView):
    """
    User login endpoint
    """
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        print("=" * 60)
        print("🔐 LOGIN ATTEMPT")
        print(f"📝 Request method: {request.method}")
        print(f"📝 Request path: {request.path}")
        print(f"📝 Request data: {request.data}")
        print(f"📝 Request headers: {dict(request.headers)}")
        print("=" * 60)
        
        username = request.data.get('username')
        password = request.data.get('password')
        
        if not username or not password:
            print("❌ Missing username or password")
            return Response({
                'status': 'error',
                'message': 'Username and password are required.',
                'errors': {'detail': 'Both username and password are required.'}
            }, status=status.HTTP_400_BAD_REQUEST)
        
        print(f"🔍 Checking user: {username}")
        
        # Try to find user
        try:
            user_obj = User.objects.get(username=username)
            print(f"✅ User found: {user_obj.username}")
            print(f"✅ User active: {user_obj.is_active}")
            print(f"✅ Password check: {user_obj.check_password(password)}")
        except User.DoesNotExist:
            print(f"❌ User not found: {username}")
            return Response({
                'status': 'error',
                'message': 'Invalid username or password.',
                'errors': {'detail': 'Invalid credentials.'}
            }, status=status.HTTP_401_UNAUTHORIZED)
        
        # Try to authenticate
        user = authenticate(username=username, password=password)
        print(f"🔑 Authenticate result: {user.username if user else 'None'}")
        
        if not user:
            # Try manual check
            if user_obj.check_password(password):
                user = user_obj
                print(f"✅ Manual authentication successful for: {user_obj.username}")
            else:
                print(f"❌ Authentication failed for: {username}")
                return Response({
                    'status': 'error',
                    'message': 'Invalid username or password.',
                    'errors': {'detail': 'Invalid credentials.'}
                }, status=status.HTTP_401_UNAUTHORIZED)
        
        if not user.is_active:
            print(f"❌ User is inactive: {username}")
            return Response({
                'status': 'error',
                'message': 'This account is deactivated.',
                'errors': {'detail': 'Account is inactive.'}
            }, status=status.HTTP_401_UNAUTHORIZED)
        
        print(f"✅ Login successful for: {user.username}")
        
        # Update last login
        user.last_login = timezone.now()
        user.save(update_fields=['last_login'])
        
        # Generate tokens
        refresh = RefreshToken.for_user(user)
        
        response_data = {
            'status': 'success',
            'message': 'Login successful.',
            'user': {
                'id': str(user.id),
                'username': user.username,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
            },
            'tokens': {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }
        }
        
        print(f"✅ Response: {response_data.keys()}")
        print("=" * 60)
        
        return Response(response_data, status=status.HTTP_200_OK)
# ============================================================
# USER LOGOUT VIEW
# ============================================================

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


# ============================================================
# USER PROFILE VIEW
# ============================================================

class UserProfileView(APIView):
    """
    Get and update user profile
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        user = request.user
        return Response({
            'status': 'success',
            'user': {
                'id': str(user.id),
                'username': user.username,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'user_type': getattr(user, 'user_type', 'student'),
                'college_name': getattr(user, 'college_name', ''),
                'year_of_study': getattr(user, 'year_of_study', None),
                'branch': getattr(user, 'branch', ''),
                'bio': getattr(user, 'bio', ''),
                'profile_picture': user.profile_picture.url if hasattr(user, 'profile_picture') and user.profile_picture else None,
                'github_username': getattr(user, 'github_username', ''),
                'total_code_reviews': getattr(user, 'total_code_reviews', 0),
                'total_bugs_found': getattr(user, 'total_bugs_found', 0),
                'average_quality_score': float(getattr(user, 'average_quality_score', 0.0)),
            }
        }, status=status.HTTP_200_OK)
    
    def patch(self, request):
        user = request.user
        allowed_fields = ['first_name', 'last_name', 'bio', 'college_name', 'branch', 'year_of_study']
        for field in allowed_fields:
            if field in request.data:
                setattr(user, field, request.data[field])
        user.save()
        
        return Response({
            'status': 'success',
            'message': 'Profile updated successfully.',
            'user': {
                'id': str(user.id),
                'username': user.username,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'user_type': getattr(user, 'user_type', 'student'),
                'college_name': getattr(user, 'college_name', ''),
                'year_of_study': getattr(user, 'year_of_study', None),
                'branch': getattr(user, 'branch', ''),
                'bio': getattr(user, 'bio', ''),
                'profile_picture': user.profile_picture.url if hasattr(user, 'profile_picture') and user.profile_picture else None,
                'github_username': getattr(user, 'github_username', ''),
                'total_code_reviews': getattr(user, 'total_code_reviews', 0),
                'total_bugs_found': getattr(user, 'total_bugs_found', 0),
                'average_quality_score': float(getattr(user, 'average_quality_score', 0.0)),
            }
        }, status=status.HTTP_200_OK)


# ============================================================
# PASSWORD CHANGE VIEW
# ============================================================

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


# ============================================================
# PASSWORD RESET REQUEST VIEW
# ============================================================

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
            PasswordResetOTP.objects.create(
                user=user,
                otp=otp,
                expires_at=timezone.now() + timezone.timedelta(minutes=10)
            )
            
            # Send email
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


# ============================================================
# PASSWORD RESET VERIFY VIEW
# ============================================================

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


# ============================================================
# PASSWORD RESET CONFIRM VIEW
# ============================================================

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


# ============================================================
# USER STATISTICS VIEW
# ============================================================

class UserStatisticsView(APIView):
    """
    Get user statistics
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        user = request.user
        
        return Response({
            'username': user.username,
            'total_code_reviews': getattr(user, 'total_code_reviews', 0),
            'total_bugs_found': getattr(user, 'total_bugs_found', 0),
            'average_quality_score': round(getattr(user, 'average_quality_score', 0), 2),
            'user_type': getattr(user, 'user_type', 'student'),
            'is_verified': getattr(user, 'is_verified', False),
            'member_since': user.date_joined.strftime('%B %d, %Y')
        }, status=status.HTTP_200_OK)


# ============================================================
# AUTH STATUS VIEW
# ============================================================

class AuthStatusView(APIView):
    """
    Check if user is authenticated
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        user = request.user
        return Response({
            'status': 'success',
            'is_authenticated': True,
            'user': {
                'id': str(user.id),
                'username': user.username,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
            }
        }, status=status.HTTP_200_OK)


# ============================================================
# ALL USERS VIEW (Admin)
# ============================================================

class AllUsersView(generics.ListAPIView):
    """
    Admin view to list all users
    """
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]
    
    def get_queryset(self):
        return User.objects.all().order_by('-date_joined')