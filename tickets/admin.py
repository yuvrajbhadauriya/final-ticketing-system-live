from django.contrib import admin, messages
from .models import Submission
from .pdf_utils import generate_ticket_pdf
from django.core.mail import EmailMessage

@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'transaction_id', 'status', 'ticket_id', 'email_sent_status')
    list_filter = ('status', 'email_sent')
    search_fields = ('full_name', 'email', 'ticket_id', 'qr_code_id')
    actions = ['send_ticket_emails']
    list_editable = ('status',)

    # Add qr_code_id to the read-only fields
    readonly_fields = ('submitted_at', 'updated_at', 'processed_by', 'ticket_id', 'qr_code_id')

    @admin.display(boolean=True, description='Email Sent?')
    def email_sent_status(self, obj):
        return obj.email_sent

    def save_model(self, request, obj, form, change):
        if obj.status == 'approved' and not obj.ticket_id:
            ticket_id_num = 2500000 + obj.id
            obj.ticket_id = f"TEDxVIPS{ticket_id_num}"
        obj.processed_by = request.user
        super().save_model(request, obj, form, change)

    @admin.action(description="Send Ticket Email to Selected")
    def send_ticket_emails(self, request, queryset):
        approved_submissions = queryset.filter(status='approved', email_sent=False)
        emails_sent = 0
        for submission in approved_submissions:
            if not submission.ticket_id:
                self.message_user(request, f"Submission for {submission.email} must be approved and saved before sending email.", level=messages.WARNING)
                continue
            pdf_buffer = generate_ticket_pdf(submission)
            try:
                email = EmailMessage(
                    "Your TEDxVIPS'25 | IGNITED Ticket is Here!",
                    f'Hi {submission.full_name},\n\nYour ticket is attached.\n\nYour Ticket ID is: {submission.ticket_id}',
                    'your_email@gmail.com',
                    [submission.email],
                )
                email.attach(f'ticket_{submission.ticket_id}.pdf', pdf_buffer.getvalue(), 'application/pdf')
                email.send()
                submission.email_sent = True
                submission.save()
                emails_sent += 1
            except Exception as e:
                self.message_user(request, f"Failed to send email to {submission.email}: {e}", level=messages.ERROR)
        if emails_sent > 0:
            self.message_user(request, f"Successfully sent {emails_sent} ticket email(s).", level=messages.SUCCESS)
        else:
            self.message_user(request, "No approved, unsent submissions were selected.", level=messages.WARNING)