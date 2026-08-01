from rest_framework import status, generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from django.http import FileResponse, HttpResponse
from django.utils import timezone
from .models import Report
from .serializers import ReportSerializer, ReportCreateSerializer, ReportGenerateSerializer
from .services import ReportService
from code_review.models import CodeSubmission, ReviewHistory
import logging

logger = logging.getLogger(__name__)

class ReportListView(generics.ListCreateAPIView):
    """
    List and create reports
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return ReportCreateSerializer
        return ReportSerializer
    
    def get_queryset(self):
        user = self.request.user
        if user.user_type == 'admin':
            return Report.objects.all()
        return Report.objects.filter(user=user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class ReportDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Get, update, or delete a specific report
    """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ReportSerializer
    
    def get_queryset(self):
        user = self.request.user
        if user.user_type == 'admin':
            return Report.objects.all()
        return Report.objects.filter(user=user)

class GenerateReportView(APIView):
    """
    Generate a report
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        serializer = ReportGenerateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({
                'status': 'error',
                'message': 'Invalid request',
                'errors': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
        
        report_id = serializer.validated_data['report_id']
        format_type = serializer.validated_data.get('format', 'pdf')
        
        try:
            report = Report.objects.get(id=report_id, user=request.user)
        except Report.DoesNotExist:
            return Response({
                'status': 'error',
                'message': 'Report not found or you do not have permission'
            }, status=status.HTTP_404_NOT_FOUND)
        
        try:
            # Get data for report
            report_data = {}
            
            if report.submission:
                submission = report.submission
                report_data['submission_title'] = submission.title
                report_data['username'] = request.user.username
                report_data['quality_score'] = submission.quality_score
                report_data['stats'] = {
                    'bug_count': submission.bug_count,
                    'issue_count': submission.issue_count,
                    'suggestion_count': submission.suggestion_count,
                }
                
                # Get review data if available
                if report.review:
                    review = report.review
                    report_data['bugs'] = review.bugs
                    report_data['issues'] = review.issues
                    report_data['suggestions'] = review.suggestions
                    report_data['explanation'] = review.explanation
                    report_data['test_cases'] = review.test_cases
                else:
                    # Try to get latest review
                    latest_review = ReviewHistory.objects.filter(submission=submission).first()
                    if latest_review:
                        report_data['bugs'] = latest_review.bugs
                        report_data['issues'] = latest_review.issues
                        report_data['suggestions'] = latest_review.suggestions
                        report_data['explanation'] = latest_review.explanation
                        report_data['test_cases'] = latest_review.test_cases
            
            # Generate report
            if format_type == 'pdf':
                file_buffer = ReportService.generate_report(report_data, 'pdf')
                
                # Save file
                filename = f"report_{report.id}_{timezone.now().strftime('%Y%m%d_%H%M%S')}.pdf"
                report.file.save(filename, ContentFile(file_buffer.getvalue()))
                report.file_size = file_buffer.getvalue().__len__()
            else:
                html_content = ReportService.generate_report(report_data, 'html')
                filename = f"report_{report.id}_{timezone.now().strftime('%Y%m%d_%H%M%S')}.html"
                report.file.save(filename, ContentFile(html_content.encode()))
                report.file_size = len(html_content)
            
            report.is_generated = True
            report.generated_at = timezone.now()
            report.save()
            
            return Response({
                'status': 'success',
                'message': 'Report generated successfully',
                'data': ReportSerializer(report).data
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            logger.error(f"Report generation failed: {str(e)}")
            return Response({
                'status': 'error',
                'message': f'Report generation failed: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class DownloadReportView(APIView):
    """
    Download a report
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request, report_id):
        try:
            report = Report.objects.get(id=report_id, user=request.user)
        except Report.DoesNotExist:
            return Response({
                'status': 'error',
                'message': 'Report not found or you do not have permission'
            }, status=status.HTTP_404_NOT_FOUND)
        
        if not report.file:
            return Response({
                'status': 'error',
                'message': 'Report file not found'
            }, status=status.HTTP_404_NOT_FOUND)
        
        report.is_downloaded = True
        report.save()
        
        response = FileResponse(report.file, as_attachment=True)
        response['Content-Disposition'] = f'attachment; filename="{report.file.name.split("/")[-1]}"'
        return response