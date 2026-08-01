from django.urls import path
from . import views

urlpatterns = [
    path('admin/', views.AdminDashboardView.as_view(), name='admin_dashboard'),
    path('user/', views.UserDashboardView.as_view(), name='user_dashboard'),
]