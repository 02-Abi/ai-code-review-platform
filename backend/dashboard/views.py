"""
Views for Dashboard App - Using code_review models
"""
from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Count, Avg, Sum
from django.contrib.auth import get_user_model

# IMPORT FROM code_review - NOT from dashboard
from code_review.models import CodeSubmission, ProgrammingLanguage

User = get_user_model()

# ============ ADMIN DASHBOARD ============

class AdminDashboardView(APIView):
    """
    Admin Dashboard - Overview statistics
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        if request.user.user_type != 'admin':
            return Response({
                'status': 'error',
                'message': 'Admin access required'
            }, status=status.HTTP_403_FORBIDDEN)
        
        try:
            total_submissions = CodeSubmission.objects.count()
            completed = CodeSubmission.objects.filter(status='completed').count()
            pending = CodeSubmission.objects.filter(status='pending').count()
            failed = CodeSubmission.objects.filter(status='failed').count()
            
            avg_score = CodeSubmission.objects.filter(
                status='completed'
            ).aggregate(avg=Avg('quality_score'))['avg'] or 0
            
            total_bugs = CodeSubmission.objects.aggregate(
                total=Sum('bug_count')
            )['total'] or 0
            
            language_stats = ProgrammingLanguage.objects.annotate(
                submission_count=Count('code_submissions')
            ).values('name', 'submission_count').order_by('-submission_count')
            
            return Response({
                'status': 'success',
                'data': {
                    'overview': {
                        'total_submissions': total_submissions,
                        'completed_reviews': completed,
                        'pending_reviews': pending,
                        'failed_reviews': failed,
                        'total_users': User.objects.count(),
                        'average_quality_score': round(avg_score, 2),
                        'total_bugs_found': total_bugs,
                    },
                    'language_stats': list(language_stats),
                }
            })
            
        except Exception as e:
            return Response({
                'status': 'error',
                'message': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# ============ USER DASHBOARD ============

class UserDashboardView(APIView):
    """
    User Dashboard - Personal statistics
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        user = request.user
        
        try:
            submissions = CodeSubmission.objects.filter(user=user)
            
            total = submissions.count()
            completed = submissions.filter(status='completed').count()
            pending = submissions.filter(status='pending').count()
            
            avg_score = submissions.filter(
                status='completed'
            ).aggregate(avg=Avg('quality_score'))['avg'] or 0
            
            total_bugs = submissions.aggregate(
                total=Sum('bug_count')
            )['total'] or 0
            
            return Response({
                'status': 'success',
                'data': {
                    'overview': {
                        'total_submissions': total,
                        'completed_reviews': completed,
                        'pending_reviews': pending,
                        'average_quality_score': round(avg_score, 2),
                        'total_bugs_found': total_bugs,
                    }
                }
            })
            
        except Exception as e:
            return Response({
                'status': 'error',
                'message': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)