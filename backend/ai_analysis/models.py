"""
Models for AI Code Review App
"""
from django.db import models
from django.conf import settings
from django.utils import timezone
import uuid


class ProgrammingLanguage(models.Model):
    """
    Programming language model
    """
    name = models.CharField(max_length=50, unique=True)
    extension = models.CharField(max_length=20, blank=True, null=True)
    icon = models.CharField(max_length=10, blank=True, null=True)
    color = models.CharField(max_length=20, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name = 'Programming Language'
        verbose_name_plural = 'Programming Languages'


class CodeSubmission(models.Model):
    """
    Code submission model
    """
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='submissions')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    code = models.TextField()
    language = models.ForeignKey(ProgrammingLanguage, on_delete=models.SET_NULL, null=True, blank=True)
    
    # Status
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    # Analysis results
    quality_score = models.IntegerField(default=0)
    bug_count = models.IntegerField(default=0)
    issue_count = models.IntegerField(default=0)
    suggestion_count = models.IntegerField(default=0)
    analysis_result = models.JSONField(default=dict, blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    reviewed_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.title} - {self.user.username}"

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Code Submission'
        verbose_name_plural = 'Code Submissions'


class ReviewHistory(models.Model):
    """
    Review history model
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    submission = models.ForeignKey(CodeSubmission, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reviews')
    
    # Review results
    quality_score = models.IntegerField(default=0)
    bugs = models.JSONField(default=list)
    issues = models.JSONField(default=list)
    suggestions = models.JSONField(default=list)
    explanation = models.TextField(blank=True, null=True)
    test_cases = models.JSONField(default=list)
    
    # AI provider info
    ai_provider = models.CharField(max_length=50, default='static_analysis')
    ai_model = models.CharField(max_length=50, default='built-in')
    ai_response = models.JSONField(default=dict, blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Review for {self.submission.title} - {self.user.username}"

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Review History'
        verbose_name_plural = 'Review Histories'


class CodeReviewComment(models.Model):
    """
    Code review comment model
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    review = models.ForeignKey(ReviewHistory, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='review_comments')
    
    line_number = models.IntegerField(null=True, blank=True)
    comment = models.TextField()
    is_resolved = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Comment by {self.user.username} on {self.review.submission.title}"

    class Meta:
        ordering = ['created_at']
        verbose_name = 'Code Review Comment'
        verbose_name_plural = 'Code Review Comments'


class CodeSnippet(models.Model):
    """
    Code snippet model for saving favorite code snippets
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='snippets')
    
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    code = models.TextField()
    language = models.ForeignKey(ProgrammingLanguage, on_delete=models.SET_NULL, null=True, blank=True)
    
    is_public = models.BooleanField(default=False)
    tags = models.JSONField(default=list, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} - {self.user.username}"

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Code Snippet'
        verbose_name_plural = 'Code Snippets'


class CodeAnalysisReport(models.Model):
    """
    Detailed code analysis report
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    submission = models.ForeignKey(CodeSubmission, on_delete=models.CASCADE, related_name='reports')
    
    # Detailed analysis
    complexity_score = models.IntegerField(default=0)
    maintainability_score = models.IntegerField(default=0)
    security_score = models.IntegerField(default=0)
    performance_score = models.IntegerField(default=0)
    documentation_score = models.IntegerField(default=0)
    
    # Detailed findings
    security_vulnerabilities = models.JSONField(default=list)
    performance_issues = models.JSONField(default=list)
    code_smells = models.JSONField(default=list)
    duplicated_code = models.JSONField(default=list)
    
    # Metrics
    lines_of_code = models.IntegerField(default=0)
    comment_ratio = models.FloatField(default=0)
    function_count = models.IntegerField(default=0)
    class_count = models.IntegerField(default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Report for {self.submission.title}"

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Code Analysis Report'
        verbose_name_plural = 'Code Analysis Reports'