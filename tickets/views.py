# --- ADD THESE IMPORTS AT THE TOP ---
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
# --- END OF NEW IMPORTS ---

from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Submission
from .forms import SubmissionForm
from .pdf_utils import generate_ticket_pdf
from pdf2image import convert_from_bytes
from io import BytesIO
import json # Import for handling JSON data

# --- Customer Facing Views ---
# (These views remain the same)
def submission_form_view(request):
    if request.method == 'POST':
        form = SubmissionForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('submission_success')
    else:
        form = SubmissionForm()
    return render(request, 'tickets/submission_form.html', {'form': form})

def submission_success_view(request):
    return render(request, 'tickets/submission_success.html')

# --- Ticket Status Views ---
# (These views remain the same)
def check_status_view(request):
    return render(request, 'tickets/check_status.html')

def status_result_view(request):
    # ... (code remains the same) ...
    email = request.POST.get('email', None)
    submission = None
    error = None
    if email:
        try:
            submission = Submission.objects.get(email__iexact=email)
        except Submission.DoesNotExist:
            error = "No submission found for this email address."
    else:
        return redirect('check_status')
    return render(request, 'tickets/status_result.html', {'submission': submission, 'error': error})

# --- Ticket Download and Preview Views ---
# (These views remain the same)
def download_ticket_view(request, submission_id):
    # ... (code remains the same) ...
    submission = get_object_or_404(Submission, id=submission_id, status='approved')
    pdf_buffer = generate_ticket_pdf(submission)
    response = HttpResponse(pdf_buffer, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="ticket_{submission.ticket_id}.pdf"'
    return response

def ticket_preview_image_view(request, submission_id):
    # ... (code remains the same) ...
    submission = get_object_or_404(Submission, id=submission_id, status='approved')
    pdf_buffer = generate_ticket_pdf(submission)
    images = convert_from_bytes(pdf_buffer.read(), first_page=1, last_page=1)
    image = images[0]
    img_buffer = BytesIO()
    image.save(img_buffer, 'PNG')
    img_buffer.seek(0)
    return HttpResponse(img_buffer, content_type='image/png')


# --- Admin Facing Views ---
# (These views remain the same)
def admin_dashboard_view(request):
    # ... (code remains the same) ...
    submissions = Submission.objects.all()
    return render(request, 'tickets/admin_dashboard.html', {'submissions': submissions})

# --- TICKET SCANNING AND VERIFICATION VIEWS ---
# --------------------------------------------------

@login_required
def scan_ticket_view(request):
    return render(request, 'tickets/scan_ticket.html')


@csrf_exempt
@login_required
def verify_ticket_api(request):
    """
    MODIFIED: This view now ONLY verifies the ticket and returns its details.
    It does NOT automatically check the person in.
    """
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            qr_code_id = data.get('qr_code_id')
            submission = Submission.objects.get(qr_code_id=qr_code_id)

            if submission.status != 'approved':
                return JsonResponse({'status': 'error', 'message': 'Ticket Not Approved'})

            if submission.checked_in:
                return JsonResponse({
                    'status': 'warning',
                    'message': 'Ticket Already Scanned',
                    'attendee': submission.full_name,
                    'email': submission.email,
                    'ticket_id': submission.ticket_id
                })

            # --- CHANGE ---
            # If all checks pass, just return the ticket details for confirmation.
            return JsonResponse({
                'status': 'success',
                'message': 'Valid Ticket Found!',
                'attendee': submission.full_name,
                'email': submission.email,
                'ticket_id': submission.ticket_id,
                'qr_code_id': submission.qr_code_id # Pass this back to use for confirmation
            })

        except Submission.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Invalid Ticket Code'})
        except Exception:
            return JsonResponse({'status': 'error', 'message': 'An unexpected error occurred.'})

    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'}, status=405)


# --- NEW FUNCTION ---
@csrf_exempt
@login_required
def confirm_check_in_api(request):
    """
    NEW: This view handles the final check-in after the staff confirms it.
    """
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            qr_code_id = data.get('qr_code_id')
            submission = Submission.objects.get(qr_code_id=qr_code_id)
            
            # Final checks before marking as checked in
            if submission.status != 'approved' or submission.checked_in:
                return JsonResponse({'status': 'error', 'message': 'Ticket cannot be checked in.'}, status=400)

            submission.checked_in = True
            submission.save()
            
            return JsonResponse({
                'status': 'confirmed', 
                'message': 'Check-In Confirmed!',
                'attendee': submission.full_name
            })

        except Submission.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Invalid Ticket Code'})
        except Exception:
            return JsonResponse({'status': 'error', 'message': 'An unexpected error occurred.'})
            
    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'}, status=405)