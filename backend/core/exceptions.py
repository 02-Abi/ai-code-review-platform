"""
Custom exception handlers for the API
"""
from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status
from django.core.exceptions import ValidationError
from django.db import IntegrityError
import logging

logger = logging.getLogger(__name__)

def custom_exception_handler(exc, context):
    """
    Custom exception handler for consistent error responses
    """
    # Call REST framework's default exception handler first
    response = exception_handler(exc, context)
    
    # If response is None, it means the exception wasn't handled by DRF
    if response is None:
        if isinstance(exc, ValidationError):
            return Response({
                'status': 'error',
                'message': 'Validation Error',
                'errors': exc.message_dict
            }, status=status.HTTP_400_BAD_REQUEST)
        
        if isinstance(exc, IntegrityError):
            return Response({
                'status': 'error',
                'message': 'Database Integrity Error',
                'detail': str(exc)
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Log unexpected errors
        logger.error(f"Unhandled exception: {exc}")
        return Response({
            'status': 'error',
            'message': 'Internal Server Error',
            'detail': str(exc) if str(exc) else 'An unexpected error occurred'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    # Customize DRF's default error response
    if response.status_code >= 400:
        response.data = {
            'status': 'error',
            'message': response.data.get('detail', 'Request failed'),
            'errors': response.data if 'detail' not in response.data else None
        }
    
    return response