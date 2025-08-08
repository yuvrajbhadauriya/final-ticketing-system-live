from django.db import models
from django.contrib.auth.models import User
import uuid # Import the library for generating random IDs

class Submission(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]

    # --- Customer and Transaction Details ---
    full_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    transaction_id = models.CharField(max_length=255)
    screenshot = models.ImageField(upload_to='screenshots/')

    # --- Admin and Status Tracking ---
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    ticket_id = models.CharField(max_length=20, unique=True, blank=True, null=True)
    email_sent = models.BooleanField(default=False)

    # --- NEW: Secure QR Code ID ---
    # This will automatically generate a unique, random ID for every new submission.
    qr_code_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    # --- Timestamps and Auditing ---
    submitted_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    processed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='processed_submissions')


    def __str__(self):
        return f"{self.full_name} ({self.email}) - {self.status}"

    class Meta:
        ordering = ['-submitted_at']