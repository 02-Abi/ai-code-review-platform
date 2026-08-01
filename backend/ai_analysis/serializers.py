"""
Serializers for AI Code Review App
"""
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import (
    ProgrammingLanguage, CodeSubmission, ReviewHistory,
    CodeReviewComment, CodeSnippet, CodeAnalysisReport
)


class UserSerializer(serializers.ModelSerializer):
    """User serializer"""
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']
        read_only_fields = ['id']


class ProgrammingLanguageSerializer(serializers.ModelSerializer):
    """Programming Language serializer"""
    class Meta:
        model = ProgrammingLanguage
        fields = ['id', 'name', 'extension', 'icon', 'color', 'is_active']
        read_only_fields = ['id', 'created_at', 'updated_at']


class CodeSubmissionSerializer(serializers.ModelSerializer):
    """Code Submission serializer"""
    user = UserSerializer(read_only=True)
    language_name = serializers.CharField(source='language.name', read_only=True)
    review_count = serializers.SerializerMethodField()
    
    class Meta:
        model = CodeSubmission
        fields = [
            'id', 'user', 'title', 'description', 'code', 'language',
            'language_name', 'status', 'quality_score', 'bug_count',
            'issue_count', 'suggestion_count', 'analysis_result',
            'created_at', 'updated_at', 'reviewed_at', 'review_count'
        ]
        read_only_fields = [
            'id', 'user', 'created_at', 'updated_at', 'reviewed_at',
            'quality_score', 'bug_count', 'issue_count', 'suggestion_count',
            'analysis_result', 'review_count'
        ]
    
    def get_review_count(self, obj):
        return obj.reviews.count()


class CodeSubmissionCreateSerializer(serializers.ModelSerializer):
    """Code Submission create serializer"""
    class Meta:
        model = CodeSubmission
        fields = ['title', 'description', 'code', 'language']
    
    def create(self, validated_data):
        user = self.context['request'].user
        return CodeSubmission.objects.create(user=user, **validated_data)


class CodeSubmissionUpdateSerializer(serializers.ModelSerializer):
    """Code Submission update serializer"""
    class Meta:
        model = CodeSubmission
        fields = ['title', 'description', 'code', 'language']


class ReviewHistorySerializer(serializers.ModelSerializer):
    """Review History serializer"""
    user = UserSerializer(read_only=True)
    submission_title = serializers.CharField(source='submission.title', read_only=True)
    
    class Meta:
        model = ReviewHistory
        fields = [
            'id', 'submission', 'submission_title', 'user', 'quality_score',
            'bugs', 'issues', 'suggestions', 'explanation', 'test_cases',
            'ai_provider', 'ai_model', 'ai_response', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'user', 'created_at', 'updated_at']


class CodeReviewCommentSerializer(serializers.ModelSerializer):
    """Code Review Comment serializer"""
    user = UserSerializer(read_only=True)
    username = serializers.CharField(source='user.username', read_only=True)
    
    class Meta:
        model = CodeReviewComment
        fields = [
            'id', 'review', 'user', 'username', 'line_number',
            'comment', 'is_resolved', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'user', 'created_at', 'updated_at']


class CodeSnippetSerializer(serializers.ModelSerializer):
    """Code Snippet serializer"""
    user = UserSerializer(read_only=True)
    language_name = serializers.CharField(source='language.name', read_only=True)
    
    class Meta:
        model = CodeSnippet
        fields = [
            'id', 'user', 'title', 'description', 'code', 'language',
            'language_name', 'is_public', 'tags', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'user', 'created_at', 'updated_at']


class CodeAnalysisReportSerializer(serializers.ModelSerializer):
    """Code Analysis Report serializer"""
    submission_title = serializers.CharField(source='submission.title', read_only=True)
    
    class Meta:
        model = CodeAnalysisReport
        fields = [
            'id', 'submission', 'submission_title', 'complexity_score',
            'maintainability_score', 'security_score', 'performance_score',
            'documentation_score', 'security_vulnerabilities',
            'performance_issues', 'code_smells', 'duplicated_code',
            'lines_of_code', 'comment_ratio', 'function_count', 'class_count',
            'created_at'
        ]
        read_only_fields = ['id', 'created_at']


# ============================================================
# AI ANALYSIS RESULT SERIALIZERS
# ============================================================

class BugSerializer(serializers.Serializer):
    """Bug serializer"""
    line = serializers.IntegerField()
    description = serializers.CharField()
    severity = serializers.CharField()
    suggestion = serializers.CharField(required=False)


class IssueSerializer(serializers.Serializer):
    """Issue serializer"""
    line = serializers.IntegerField()
    description = serializers.CharField()
    type = serializers.CharField()
    suggestion = serializers.CharField(required=False)


class SuggestionSerializer(serializers.Serializer):
    """Suggestion serializer"""
    line = serializers.IntegerField()
    title = serializers.CharField()
    icon = serializers.CharField(required=False)
    description = serializers.CharField()
    why = serializers.CharField(required=False)
    how = serializers.CharField(required=False)
    code_example = serializers.CharField(required=False)
    benefits = serializers.ListField(child=serializers.CharField(), required=False)


class TestCaseSerializer(serializers.Serializer):
    """Test case serializer"""
    name = serializers.CharField()
    input = serializers.CharField()
    expected = serializers.CharField()
    description = serializers.CharField(required=False)


class AnalysisResultSerializer(serializers.Serializer):
    """Analysis result serializer"""
    quality_score = serializers.IntegerField()
    bugs = BugSerializer(many=True)
    issues = IssueSerializer(many=True)
    suggestions = SuggestionSerializer(many=True)
    explanation = serializers.CharField()
    test_cases = TestCaseSerializer(many=True)
    language_detected = serializers.CharField(required=False)


# ============================================================
# STATS SERIALIZERS
# ============================================================

class CodeReviewStatsSerializer(serializers.Serializer):
    """Code review statistics serializer"""
    total_submissions = serializers.IntegerField()
    completed_reviews = serializers.IntegerField()
    pending_reviews = serializers.IntegerField()
    total_bugs_found = serializers.IntegerField()
    average_quality_score = serializers.FloatField()
    total_issues = serializers.IntegerField(required=False)
    total_suggestions = serializers.IntegerField(required=False)


class LanguageStatsSerializer(serializers.Serializer):
    """Language statistics serializer"""
    language = serializers.CharField()
    total_submissions = serializers.IntegerField()
    average_score = serializers.FloatField()
    total_bugs = serializers.IntegerField()


class UserActivitySerializer(serializers.Serializer):
    """User activity serializer"""
    date = serializers.DateField()
    submissions = serializers.IntegerField()
    reviews = serializers.IntegerField()


# ============================================================
# FILE UPLOAD SERIALIZERS
# ============================================================

class CodeUploadSerializer(serializers.Serializer):
    """Code file upload serializer"""
    file = serializers.FileField()
    title = serializers.CharField(max_length=200, required=False)
    description = serializers.CharField(required=False)
    language = serializers.IntegerField(required=False)
    
    def validate_file(self, value):
        """Validate uploaded file"""
        # Check file size (max 5MB)
        if value.size > 5 * 1024 * 1024:
            raise serializers.ValidationError("File size should not exceed 5MB")
        
        # Check file extension
        allowed_extensions = [
            '.py', '.js', '.ts', '.jsx', '.tsx', '.java', '.c', '.cpp',
            '.cc', '.cxx', '.h', '.hpp', '.cs', '.go', '.rs', '.rb',
            '.php', '.html', '.htm', '.css', '.sql', '.swift', '.kt',
            '.kts', '.scala', '.pl', '.pm', '.r', '.dart', '.exs',
            '.ex', '.hs', '.lhs', '.lua', '.jl', '.sh', '.bash',
            '.zsh', '.ps1', '.psm1', '.psd1', '.json', '.xml', '.yaml',
            '.yml', '.toml', '.md', '.txt'
        ]
        
        import os
        ext = os.path.splitext(value.name)[1].lower()
        if ext and ext not in allowed_extensions:
            raise serializers.ValidationError(f"File type {ext} is not supported")
        
        return value


class CodeBatchAnalyzeSerializer(serializers.Serializer):
    """Batch analyze serializer"""
    submissions = serializers.ListField(
        child=serializers.IntegerField(),
        help_text="List of submission IDs to analyze"
    )
    language = serializers.IntegerField(required=False)


# ============================================================
# DETECT LANGUAGE SERIALIZER
# ============================================================

class DetectLanguageSerializer(serializers.Serializer):
    """Detect language serializer"""
    code = serializers.CharField(required=True)
    filename = serializers.CharField(required=False)


# ============================================================
# FILTER SERIALIZERS
# ============================================================

class SubmissionFilterSerializer(serializers.Serializer):
    """Submission filter serializer"""
    language = serializers.IntegerField(required=False)
    status = serializers.ChoiceField(choices=['pending', 'processing', 'completed', 'failed'], required=False)
    date_from = serializers.DateField(required=False)
    date_to = serializers.DateField(required=False)
    search = serializers.CharField(required=False)
    sort_by = serializers.ChoiceField(
        choices=['created_at', 'quality_score', 'bug_count'],
        default='created_at'
    )
    sort_order = serializers.ChoiceField(
        choices=['asc', 'desc'],
        default='desc'
    )


class ReviewFilterSerializer(serializers.Serializer):
    """Review filter serializer"""
    submission_id = serializers.IntegerField(required=False)
    user_id = serializers.IntegerField(required=False)
    min_score = serializers.IntegerField(required=False, min_value=0, max_value=100)
    max_score = serializers.IntegerField(required=False, min_value=0, max_value=100)
    date_from = serializers.DateField(required=False)
    date_to = serializers.DateField(required=False)