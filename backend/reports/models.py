from django.db import models

# Create your models here.
from django.db import models
from django.conf import settings
import uuid

class Report(models.Model):
    """
    Report model for generated code review reports
    """
    REPORT_TYPES = (
        ('code_review', 'Code Review'),
        ('bug_report', 'Bug Report'),
        ('quality_report', 'Quality Report'),
        ('summary', 'Summary Report'),
    )
    
    FORMATS = (
        ('pdf', 'PDF'),
        ('html', 'HTML'),
        ('json', 'JSON'),
    )
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reports')
    submission = models.ForeignKey('code_review.CodeSubmission', on_delete=models.CASCADE, null=True, blank=True)
    review = models.ForeignKey('code_review.ReviewHistory', on_delete=models.CASCADE, null=True, blank=True)
    
    title = models.CharField(max_length=200)
    report_type = models.CharField(max_length=20, choices=REPORT_TYPES, default='code_review')
    format = models.CharField(max_length=10, choices=FORMATS, default='pdf')
    
    # File storage
    file = models.FileField(upload_to='reports/%Y/%m/%d/', null=True, blank=True)
    file_size = models.IntegerField(default=0)
    
    # Content
    content = models.JSONField(default=dict)
    
    # Status
    is_generated = models.BooleanField(default=False)
    is_downloaded = models.BooleanField(default=False)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    generated_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        db_table = 'reports'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', '-created_at']),
            models.Index(fields=['report_type']),
        ]
    
    def __str__(self):
        return f"{self.title} - {self.user.username}"
    
    def get_file_url(self):
        if self.file:
            return self.file.url
        return None