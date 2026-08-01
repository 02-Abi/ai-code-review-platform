from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

def home(request):
    """
    Home page view - API information
    """
    return JsonResponse({
        'status': 'success',
        'message': 'Welcome to AI-Powered Code Review and Bug Detection Platform',
        'version': '1.0.0',
        'endpoints': {
            'documentation': '/swagger/',
            'admin': '/admin/',
            'api': {
                'accounts': '/api/accounts/',
                'code_review': '/api/code-review/',
                'ai_analysis': '/api/ai-analysis/',
                'dashboard': '/api/dashboard/',
                'reports': '/api/reports/',
            },
            'auth': {
                'login': '/api/token/',
                'refresh': '/api/token/refresh/',
                'verify': '/api/token/verify/',
            }
        },
        'documentation': {
            'swagger': '/swagger/',
            'redoc': '/redoc/'
        }
    })