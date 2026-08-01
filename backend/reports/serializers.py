from rest_framework import serializers
from .models import Report

class ReportSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    
    class Meta:
        model = Report
        fields = (
            'id', 'user', 'username', 'submission', 'review',
            'title', 'report_type', 'format', 'file', 'file_size',
            'content', 'is_generated', 'is_downloaded',
            'created_at', 'updated_at', 'generated_at'
        )
        read_only_fields = ('id', 'user', 'username', 'created_at', 'updated_at', 'generated_at')

class ReportCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = ('title', 'report_type', 'format', 'submission', 'review')

class ReportGenerateSerializer(serializers.Serializer):
    report_id = serializers.UUIDField(required=True)
    format = serializers.ChoiceField(choices=['pdf', 'html'], default='pdf')