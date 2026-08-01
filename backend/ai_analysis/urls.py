from django.urls import path
from . import views

app_name = 'ai_analysis'

urlpatterns = [
    # Main analysis endpoints
    path('analyze/', views.CodeAnalysisView.as_view(), name='analyze'),
    path('test-cases/', views.GenerateTestCasesView.as_view(), name='test_cases'),
    path('explain/', views.ExplainCodeView.as_view(), name='explain'),
    path('static-analysis/', views.StaticAnalysisView.as_view(), name='static_analysis'),
    
    # Health check
    path('health/', views.HealthCheckView.as_view(), name='health'),
]