from django.contrib import admin

# Register your models here.
"""
Admin configuration for Code Review App
"""
from django.contrib import admin
from .models import (
    ProgrammingLanguage, CodeSubmission, ReviewHistory,
    CodeReviewComment, CodeSnippet
)

@admin.register(ProgrammingLanguage)
class ProgrammingLanguageAdmin(admin.ModelAdmin):
    list_display = ('name', 'extension', 'version', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('name', 'extension')
    ordering = ('name',)

@admin.register(CodeSubmission)
class CodeSubmissionAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'language', 'status', 'quality_score', 'created_at')
    list_filter = ('status', 'language', 'created_at')
    search_fields = ('title', 'user__username', 'code')
    readonly_fields = ('id', 'created_at', 'updated_at', 'reviewed_at')
    ordering = ('-created_at',)
    fieldsets = (
        ('Basic Information', {
            'fields': ('id', 'user', 'language', 'title', 'description')
        }),
        ('Code Content', {
            'fields': ('code', 'file', 'file_name')
        }),
        ('Review Status', {
            'fields': ('status', 'quality_score', 'bug_count', 'issue_count', 'suggestion_count')
        }),
        ('Analysis', {
            'fields': ('analysis_result',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at', 'reviewed_at')
        }),
    )

@admin.register(ReviewHistory)
class ReviewHistoryAdmin(admin.ModelAdmin):
    list_display = ('submission', 'user', 'quality_score', 'ai_provider', 'created_at')
    list_filter = ('ai_provider', 'created_at')
    search_fields = ('submission__title', 'user__username')
    readonly_fields = ('id', 'created_at')
    ordering = ('-created_at',)

@admin.register(CodeReviewComment)
class CodeReviewCommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'review', 'comment_type', 'created_at')
    list_filter = ('comment_type', 'created_at')
    search_fields = ('user__username', 'content')
    ordering = ('-created_at',)

@admin.register(CodeSnippet)
class CodeSnippetAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'language', 'is_public', 'is_favorite', 'created_at')
    list_filter = ('language', 'is_public', 'is_favorite')
    search_fields = ('title', 'user__username', 'code')
    ordering = ('-created_at',)