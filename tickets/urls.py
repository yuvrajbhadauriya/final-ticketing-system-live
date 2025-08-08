from django.urls import path
from . import views

urlpatterns = [
    path('', views.submission_form_view, name='submission_form'),
    path('success/', views.submission_success_view, name='submission_success'),
    path('check-status/', views.check_status_view, name='check_status'),
    path('status-result/', views.status_result_view, name='status_result'),
    path('download-ticket/<int:submission_id>/', views.download_ticket_view, name='download_ticket'),

    # NEW: Ticket Preview URL
    path('preview-ticket/<int:submission_id>/', views.ticket_preview_image_view, name='ticket_preview'),

    path('admin-dashboard/', views.admin_dashboard_view, name='admin_dashboard'),
    path('approve/<int:submission_id>/', views.approve_submission_view, name='approve_submission'),
    path('reject/<int:submission_id>/', views.reject_submission_view, name='reject_submission'),
]