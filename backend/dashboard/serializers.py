from rest_framework import serializers
from .models import (
    ProgrammingLanguage,
    CodeSubmission,
    ReviewHistory,
    CodeReviewComment,
    CodeSnippet
)


class ProgrammingLanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProgrammingLanguage
        fields = "__all__"


class CodeSubmissionSerializer(serializers.ModelSerializer):
    language_name = serializers.CharField(source="language.name", read_only=True)

    class Meta:
        model = CodeSubmission
        fields = "__all__"


class CodeSubmissionCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CodeSubmission
        fields = [
            "title",
            "language",
            "code"
        ]


class ReviewHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ReviewHistory
        fields = "__all__"


class CodeReviewCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = CodeReviewComment
        fields = "__all__"


class CodeSnippetSerializer(serializers.ModelSerializer):
    language_name = serializers.CharField(source="language.name", read_only=True)

    class Meta:
        model = CodeSnippet
        fields = "__all__"