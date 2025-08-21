from django.db import models
from django.contrib.auth.models import User
import uuid # Import the library for generating random IDs

class Submission(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    
    TICKET_TYPE_CHOICES = [
        ('vips', 'VIPS Student'),
        ('outsider', 'Outsider'),
    ]
    
    PASS_TYPE_CHOICES = [
        ('day1', 'Day 1 Pass'),
        ('combo', 'Combo Pass'),
    ]

    attendee_type = models.CharField(max_length=10, choices=TICKET_TYPE_CHOICES, default='outsider')
    vips_id_card = models.ImageField(upload_to='vips_ids/', blank=True, null=True)
    pass_type = models.CharField(max_length=10, choices=PASS_TYPE_CHOICES, default='day1')
    full_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    transaction_id = models.CharField(max_length=255)
    screenshot = models.ImageField(upload_to='screenshots/', blank=True, null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    ticket_id = models.CharField(max_length=20, unique=True, blank=True, null=True)
    email_sent = models.BooleanField(default=False)
    checked_in = models.BooleanField(default=False)
    qr_code_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    submitted_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    processed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='processed_submissions')


    def __str__(self):
        return f"{self.full_name} ({self.email}) - {self.status}"

    class Meta:
        ordering = ['-submitted_at']
        permissions = [
            ("can_edit_kiosk_submission", "Can edit kiosk submission details"),
            ("can_change_status_fields", "Can change email sent and checked in status"),
        ]

# --- NEW: Kiosk Request Model ---
# This model will store temporary requests from the kiosk customer form.
class KioskRequest(models.Model):
    full_name = models.CharField(max_length=255)
    email = models.EmailField()
    attendee_type = models.CharField(max_length=10, choices=Submission.TICKET_TYPE_CHOICES)
    pass_type = models.CharField(max_length=10, choices=Submission.PASS_TYPE_CHOICES)
    cash_amount = models.IntegerField()
    
    # This links the request to a specific staff member
    assigned_to = models.ForeignKey(User, on_delete=models.CASCADE, related_name='kiosk_requests')
    
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Request from {self.full_name} for {self.assigned_to.username}"

    class Meta:
        ordering = ['-created_at']
