from django.urls import path
from . import views

app_name = 'code_review'

urlpatterns = [
    # Programming Languages
    path('languages/', views.ProgrammingLanguageListView.as_view(), name='languages'),
    
    # Submissions
    path('submissions/', views.CodeSubmissionListView.as_view(), name='submissions'),
    path('submissions/<uuid:pk>/', views.CodeSubmissionDetailView.as_view(), name='submission_detail'),
    path('submissions/<uuid:pk>/status/', views.CodeSubmissionStatusView.as_view(), name='submission_status'),
    
    # Review History
    path('history/', views.ReviewHistoryListView.as_view(), name='review_history'),
    path('history/<uuid:pk>/', views.ReviewHistoryDetailView.as_view(), name='review_history_detail'),
    
    # Comments
    path('reviews/<uuid:review_id>/comments/', views.CodeReviewCommentView.as_view(), name='review_comments'),
    
    # Snippets
    path('snippets/', views.CodeSnippetView.as_view(), name='snippets'),
    path('snippets/<uuid:pk>/', views.CodeSnippetDetailView.as_view(), name='snippet_detail'),
    
    # AI Review
    path('initiate-review/', views.InitiateCodeReviewView.as_view(), name='initiate_review'),
    
    # Statistics
    path('stats/', views.CodeReviewStatsView.as_view(), name='review_stats'),
]