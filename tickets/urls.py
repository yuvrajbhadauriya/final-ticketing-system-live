from django.urls import path
from . import views

urlpatterns = [
    # --- CHANGE: The main page is now the home view ---
    path('', views.home_view, name='home'),

    # --- NEW: URLs for the two separate submission forms ---
    path('submit/vips/', views.vips_submission_view, name='vips_submission'),
    path('submit/outsider/', views.outsider_submission_view, name='outsider_submission'),

    # --- Other URLs remain the same ---
    path('success/', views.submission_success_view, name='submission_success'),
    path('check-status/', views.check_status_view, name='check_status'),
    path('status-result/', views.status_result_view, name='status_result'),
    path('download-ticket/<int:submission_id>/', views.download_ticket_view, name='download_ticket'),
    path('preview-ticket/<int:submission_id>/', views.ticket_preview_image_view, name='ticket_preview'),

    # --- Ticket Scanning URLs ---
    path('scan/', views.scan_ticket_view, name='scan_ticket'),
    path('api/verify-ticket/', views.verify_ticket_api, name='verify_ticket_api'),
    path('api/confirm-check-in/', views.confirm_check_in_api, name='confirm_check_in_api'),
]