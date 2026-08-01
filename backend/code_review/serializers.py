"""
Serializers for Code Review App
"""
from rest_framework import serializers
from django.core.validators import MinValueValidator, MaxValueValidator
from .models import (
    ProgrammingLanguage, CodeSubmission, ReviewHistory, 
    CodeReviewComment, CodeSnippet
)

class ProgrammingLanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProgrammingLanguage
        fields = ('id', 'name', 'extension', 'version', 'is_active')
        read_only_fields = ('id',)

class CodeSubmissionSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    language_name = serializers.CharField(source='language.name', read_only=True)
    
    class Meta:
        model = CodeSubmission
        fields = (
            'id', 'user', 'username', 'language', 'language_name',
            'title', 'code', 'description', 'file', 'file_name',
            'status', 'quality_score', 'bug_count', 'issue_count',
            'suggestion_count', 'analysis_result', 'created_at', 
            'updated_at', 'reviewed_at'
        )
        read_only_fields = (
            'id', 'user', 'username', 'status', 'quality_score',
            'bug_count', 'issue_count', 'suggestion_count',
            'analysis_result', 'created_at', 'updated_at', 'reviewed_at'
        )

class CodeSubmissionCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CodeSubmission
        fields = ('id', 'language', 'title', 'code', 'description')
        read_only_fields = ('id',)

    def validate(self, data):
        if not data.get('code') and not self.initial_data.get('file'):
            raise serializers.ValidationError("Either code or file must be provided.")
        if not data.get('title'):
            raise serializers.ValidationError("Title is required.")
        if not data.get('language'):
            raise serializers.ValidationError("Language is required.")
        return data

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)

class ReviewHistorySerializer(serializers.ModelSerializer):
    submission_title = serializers.CharField(source='submission.title', read_only=True)
    username = serializers.CharField(source='user.username', read_only=True)
    
    class Meta:
        model = ReviewHistory
        fields = (
            'id', 'submission', 'submission_title', 'user', 'username',
            'quality_score', 'bugs', 'issues', 'suggestions', 
            'explanation', 'test_cases', 'ai_provider', 'ai_model',
            'created_at'
        )
        read_only_fields = ('id', 'created_at')

class CodeReviewCommentSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    
    class Meta:
        model = CodeReviewComment
        fields = ('id', 'review', 'user', 'username', 'comment_type', 
                 'content', 'line_number', 'created_at', 'updated_at')
        read_only_fields = ('id', 'user', 'username', 'created_at', 'updated_at')

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)

class CodeSnippetSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    language_name = serializers.CharField(source='language.name', read_only=True)
    
    class Meta:
        model = CodeSnippet
        fields = (
            'id', 'user', 'username', 'language', 'language_name',
            'title', 'code', 'description', 'tags', 'is_public',
            'is_favorite', 'created_at', 'updated_at'
        )
        read_only_fields = ('id', 'user', 'username', 'created_at', 'updated_at')

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)