from django.urls import path
from . import views

urlpatterns = [
    # --- Main Site URLs ---
    path('', views.home_view, name='home'),
    path('submit/vips/', views.vips_submission_view, name='vips_submission'),
    path('submit/outsider/', views.outsider_submission_view, name='outsider_submission'),
    path('success/', views.submission_success_view, name='submission_success'),
    path('check-status/', views.check_status_view, name='check_status'),
    path('status-result/', views.status_result_view, name='status_result'),
    path('download-ticket/<int:submission_id>/', views.download_ticket_view, name='download_ticket'),
    path('preview-ticket/<int:submission_id>/', views.ticket_preview_image_view, name='ticket_preview'),

    # --- Ticket Scanning URLs ---
    path('scan/', views.scan_ticket_view, name='scan_ticket'),
    path('api/verify-ticket/', views.verify_ticket_api, name='verify_ticket_api'),
    path('api/confirm-check-in/', views.confirm_check_in_api, name='confirm_check_in_api'),

    # --- Kiosk Workflow URLs ---
    path('kiosk/request/', views.kiosk_request_view, name='kiosk_request'),
    path('kiosk/success/', views.kiosk_request_success_view, name='kiosk_request_success'),
    path('kiosk/dashboard/', views.kiosk_staff_dashboard_view, name='kiosk_staff_dashboard'),
    path('kiosk/accept/<int:request_id>/', views.accept_kiosk_request_view, name='accept_kiosk_request'),
    # --- ADD THIS NEW LINE ---
    path('kiosk/reject/<int:request_id>/', views.reject_kiosk_request_view, name='reject_kiosk_request'),
]
