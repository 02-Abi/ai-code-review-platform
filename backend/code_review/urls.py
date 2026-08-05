# code_review/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('languages/', views.ProgrammingLanguageListView.as_view(), name='languages'),
    path('submissions/', views.CodeSubmissionListView.as_view(), name='submissions'),
    path('submissions/<uuid:pk>/', views.CodeSubmissionDetailView.as_view(), name='submission-detail'),
    path('submissions/<uuid:pk>/status/', views.CodeSubmissionStatusView.as_view(), name='submission-status'),
    path('reviews/', views.ReviewHistoryListView.as_view(), name='reviews'),
    path('reviews/<uuid:pk>/', views.ReviewHistoryDetailView.as_view(), name='review-detail'),
    path('reviews/<uuid:review_id>/comments/', views.CodeReviewCommentView.as_view(), name='review-comments'),
    path('snippets/', views.CodeSnippetView.as_view(), name='snippets'),
    path('snippets/<uuid:pk>/', views.CodeSnippetDetailView.as_view(), name='snippet-detail'),
    path('stats/', views.CodeReviewStatsView.as_view(), name='stats'),
    path('initiate/', views.InitiateCodeReviewView.as_view(), name='initiate-review'),
    path('detect-language/', views.DetectLanguageView.as_view(), name='detect-language'),
    path('llm-status/', views.LLMStatusView.as_view(), name='llm-status'),
]