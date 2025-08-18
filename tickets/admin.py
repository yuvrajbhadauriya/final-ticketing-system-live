from django.contrib import admin, messages
from .models import Submission
from .pdf_utils import generate_ticket_pdf
from django.core.mail import EmailMultiAlternatives # Import for HTML emails
from import_export.admin import ImportExportModelAdmin
from django.utils.html import format_html # Import for displaying images

@admin.register(Submission)
class SubmissionAdmin(ImportExportModelAdmin):
    list_display = ('full_name', 'email', 'attendee_type', 'pass_type', 'transaction_id', 'ticket_id', 'status', 'email_sent', 'checked_in')
    
    list_filter = ('status', 'attendee_type', 'pass_type', 'checked_in', 'email_sent')
    
    search_fields = ('full_name', 'email', 'ticket_id', 'transaction_id')
    actions = ['send_ticket_emails']
    list_editable = ('status',)

    readonly_fields = (
        'submitted_at', 'updated_at', 'processed_by', 'ticket_id', 
        'qr_code_id', 'vips_id_card_preview', 'screenshot_preview'
    )

    fieldsets = (
        ('Submission Details', {
            'fields': ('full_name', 'email', 'attendee_type', 'pass_type', 'transaction_id')
        }),
        ('Verification Images', {
            'fields': ('screenshot', 'screenshot_preview', 'vips_id_card', 'vips_id_card_preview')
        }),
        ('Admin Tracking', {
            'fields': ('status', 'ticket_id', 'qr_code_id', 'checked_in', 'email_sent', 'processed_by')
        }),
        ('Timestamps', {
            'fields': ('submitted_at', 'updated_at')
        }),
    )

    @admin.display(description='VIPS ID Preview')
    def vips_id_card_preview(self, obj):
        if obj.vips_id_card:
            return format_html('<a href="{0}" target="_blank"><img src="{0}" width="150" height="100" /></a>', obj.vips_id_card.url)
        return "No ID uploaded"

    @admin.display(description='Screenshot Preview')
    def screenshot_preview(self, obj):
        if obj.screenshot:
            return format_html('<a href="{0}" target="_blank"><img src="{0}" width="150" height="100" /></a>', obj.screenshot.url)
        return "No screenshot uploaded"

    def get_readonly_fields(self, request, obj=None):
        fields = list(super().get_readonly_fields(request, obj))
        
        # Check for the two custom permissions
        can_edit_details = request.user.has_perm('tickets.can_edit_kiosk_submission')
        can_edit_status_fields = request.user.has_perm('tickets.can_change_status_fields')

        # If the user is a superuser, they can edit everything
        if request.user.is_superuser:
            return fields

        # If they are not a superuser, apply restrictions
        if not can_edit_details:
            fields.extend([
                'full_name', 
                'email', 
                'attendee_type',
                'pass_type',
                'transaction_id',
            ])
        
        if not can_edit_status_fields:
            fields.extend(['checked_in', 'email_sent'])

        return tuple(fields)

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
                subject = "TICKET FOR IGNITED 2025"
                from_email = 'your_email@gmail.com' # Make sure to use your actual sender email
                to = [submission.email]

                text_content = f"""
                Hi {submission.full_name},
                
                CONGRATS FOR SECURING YOUR PASS FOR IGNITED 2025.
                We assure you that you are going to have the best time. Thank you for being a part of this legacy.
                
                Your ticket is attached below.
                
                Important Information:
                - Your ticket will be downloadable on the "Check Ticket Status" page.
                - Each ticket contains a unique QR code and will be scanned only once for entry.
                - Re-entry or second scans will not be permitted.
                
                See you at the event,
                Event Management Team
                IGNITED | TEDxVIPS 2025
                """

                html_content = f"""
                <div style="font-family: Arial, sans-serif; color: #333; max-width: 600px; margin: auto; border: 1px solid #ddd; padding: 20px;">
                    <h2 style="color: #eb0028;">CONGRATS FOR SECURING YOUR PASS FOR IGNITED 2025</h2>
                    <p>Hi {submission.full_name},</p>
                    <p>We assure you that you are going to have the best time. Thank you for being a part of this legacy.</p>
                    <p><b>Your ticket is attached below.</b></p>
                    
                    <div style="margin-top: 20px; padding-top: 15px; border-top: 1px solid #eee;">
                        <p style="font-weight: bold; color: #888888;">Important Information:</p>
                        <ul style="color: #888888; font-size: 14px; list-style-type: disc; padding-left: 20px;">
                            <li>Your ticket will be downloadable on the "Check Ticket Status" page and will also be mailed to you upon approval.</li>
                            <li>A wristband will be provided to you on the day of the event at the venue.</li>
                            <li>Each ticket contains a unique QR code and will be scanned only once for entry.</li>
                            <li>Re-entry or second scans will not be permitted.</li>
                        </ul>
                    </div>

                    <div style="margin-top: 25px; text-align: center;">
                        <p>You can also check and download your ticket from here:</p>
                        <a href="https://tedxvips2025tickets.pythonanywhere.com/check-status/" style="background-color: #eb0028; color: #ffffff; padding: 12px 25px; text-decoration: none; border-radius: 5px; font-weight: bold; display: inline-block;">Check Ticket Status</a>
                    </div>

                    <div style="margin-top: 25px; font-size: 14px; text-align: center;">
                        <p>For queries, <a href="https://wa.me/916398979052?text=Hello,%20I%20have%20some%20query/issue%20related%20to%20tickets%20for%20IGNITED'25" style="color: #eb0028; font-weight: bold;">contact us on WhatsApp</a> or reply to this email.</p>
                    </div>

                    <div style="margin-top: 30px; padding-top: 15px; border-top: 1px solid #eee; font-size: 12px; color: #999;">
                        <p>See you at the event,<br>
                        <b>Event Management Team</b><br>
                        IGNITED | TEDxVIPS 2025</p>
                    </div>
                </div>
                """

                msg = EmailMultiAlternatives(subject, text_content, from_email, to)
                msg.attach_alternative(html_content, "text/html")
                
                msg.attach(f'ticket_{submission.ticket_id}.pdf', pdf_buffer.getvalue(), 'application/pdf')
                
                msg.send()
                
                submission.email_sent = True
                submission.save()
                emails_sent += 1
            except Exception as e:
                self.message_user(request, f"Failed to send email to {submission.email}: {e}", level=messages.ERROR)

        if emails_sent > 0:
            self.message_user(request, f"Successfully sent {emails_sent} ticket email(s).", level=messages.SUCCESS)
        else:
            self.message_user(request, "No approved, unsent submissions were selected.", level=messages.WARNING)
