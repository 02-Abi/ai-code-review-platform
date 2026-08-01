"""
Models for Code Review App
"""
from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
import uuid

class ProgrammingLanguage(models.Model):
    """
    Programming languages supported by the platform
    """
    name = models.CharField(max_length=50, unique=True)
    extension = models.CharField(max_length=10)
    version = models.CharField(max_length=20, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'programming_languages'
        ordering = ['name']

    def __str__(self):
        return self.name

class CodeSubmission(models.Model):
    """
    Model for code submissions by students
    """
    STATUS_CHOICES = (
        ('pending', 'Pending Review'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='code_submissions')
    language = models.ForeignKey(ProgrammingLanguage, on_delete=models.CASCADE)
    
    # Code content
    title = models.CharField(max_length=200)
    code = models.TextField()
    description = models.TextField(blank=True, null=True)
    
    # File upload
    file = models.FileField(upload_to='code_submissions/%Y/%m/%d/', blank=True, null=True)
    file_name = models.CharField(max_length=255, blank=True, null=True)
    
    # Status
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    # Review results
    quality_score = models.FloatField(default=0.0, validators=[MinValueValidator(0), MaxValueValidator(100)])
    bug_count = models.IntegerField(default=0)
    issue_count = models.IntegerField(default=0)
    suggestion_count = models.IntegerField(default=0)
    
    # Analysis data
    analysis_result = models.JSONField(default=dict, blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    reviewed_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'code_submissions'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', '-created_at']),
            models.Index(fields=['language']),
            models.Index(fields=['status']),
        ]

    def __str__(self):
        return f"{self.title} by {self.user.username}"

    def get_absolute_url(self):
        return f"/submissions/{self.id}/"

    def save(self, *args, **kwargs):
        if self.status == 'completed' and not self.reviewed_at:
            self.reviewed_at = models.DateTimeField.auto_now_add
        super().save(*args, **kwargs)

class ReviewHistory(models.Model):
    """
    History of code reviews performed
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    submission = models.ForeignKey(CodeSubmission, on_delete=models.CASCADE, related_name='review_history')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    
    # Review results
    quality_score = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(100)])
    bugs = models.JSONField(default=list)
    issues = models.JSONField(default=list)
    suggestions = models.JSONField(default=list)
    explanation = models.TextField(blank=True, null=True)
    test_cases = models.JSONField(default=list)
    
    # AI analysis data
    ai_provider = models.CharField(max_length=50, default='openai')
    ai_model = models.CharField(max_length=100)
    ai_response = models.JSONField(default=dict)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'review_history'
        ordering = ['-created_at']

    def __str__(self):
        return f"Review for {self.submission.title} at {self.created_at}"

class CodeReviewComment(models.Model):
    """
    Comments on code reviews
    """
    COMMENT_TYPES = (
        ('bug', 'Bug'),
        ('suggestion', 'Suggestion'),
        ('improvement', 'Improvement'),
        ('question', 'Question'),
        ('note', 'Note'),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    review = models.ForeignKey(ReviewHistory, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    
    comment_type = models.CharField(max_length=20, choices=COMMENT_TYPES, default='note')
    content = models.TextField()
    line_number = models.IntegerField(blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'code_review_comments'
        ordering = ['created_at']

    def __str__(self):
        return f"Comment by {self.user.username} on {self.review}"

class CodeSnippet(models.Model):
    """
    Saved code snippets for quick access
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='snippets')
    language = models.ForeignKey(ProgrammingLanguage, on_delete=models.CASCADE)
    
    title = models.CharField(max_length=200)
    code = models.TextField()
    description = models.TextField(blank=True, null=True)
    tags = models.JSONField(default=list)
    
    is_public = models.BooleanField(default=False)
    is_favorite = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'code_snippets'
        ordering = ['-created_at']

    def __str__(self):
        return self.title