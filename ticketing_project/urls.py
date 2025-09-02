"""
URL configuration for ticketing_project project.
"""
from django.contrib import admin
from django.urls import path, include
# --- FIX: Import settings and static ---
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('tickets.urls')),
]

# --- FIX: Add this block to serve media files when DEBUG is False ---
# This tells Django how to find and serve your uploaded screenshots and IDs on the live server.
if not settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

