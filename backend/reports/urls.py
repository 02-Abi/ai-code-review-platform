from django.urls import path
from . import views

app_name = 'reports'

urlpatterns = [
    path('', views.ReportListView.as_view(), name='report_list'),
    path('<uuid:pk>/', views.ReportDetailView.as_view(), name='report_detail'),
    path('generate/', views.GenerateReportView.as_view(), name='generate_report'),
    path('download/<uuid:report_id>/', views.DownloadReportView.as_view(), name='download_report'),
]