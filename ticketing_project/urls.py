"""
URL configuration for ticketing_project project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('tickets.urls')), # Includes all URLs from your tickets app
]

# This block is for LOCAL DEVELOPMENT ONLY.
# It tells Django's local test server how to serve user-uploaded media files.
# On your live PythonAnywhere server, this code is ignored, and the "Static files"
# mapping you configured on the "Web" tab is used instead.
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

