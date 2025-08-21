# --- ADD THESE IMPORTS AT THE TOP ---
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils import timezone
from datetime import timedelta
# --- END OF NEW IMPORTS ---

from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Submission, KioskRequest # Import KioskRequest
# --- CHANGE: Import the new KioskRequestForm ---
from .forms import VipsSubmissionForm, OutsiderSubmissionForm, KioskRequestForm
from .pdf_utils import generate_ticket_pdf
from pdf2image import convert_from_bytes
from io import BytesIO
import json

# --- Main Homepage View ---
def home_view(request):
    return render(request, 'tickets/home.html')

# --- Online Submission Views ---
def vips_submission_view(request):
    if request.method == 'POST':
        form = VipsSubmissionForm(request.POST, request.FILES)
        if form.is_valid():
            submission = form.save(commit=False)
            submission.attendee_type = 'vips'
            submission.pass_type = request.POST.get('pass_type') # Get pass_type from hidden input
            submission.save()
            return redirect('submission_success')
    else:
        form = VipsSubmissionForm()
    return render(request, 'tickets/vips_submission_form.html', {'form': form})

def outsider_submission_view(request):
    if request.method == 'POST':
        form = OutsiderSubmissionForm(request.POST, request.FILES)
        if form.is_valid():
            submission = form.save(commit=False)
            submission.attendee_type = 'outsider'
            submission.pass_type = request.POST.get('pass_type') # Get pass_type from hidden input
            submission.save()
            return redirect('submission_success')
    else:
        form = OutsiderSubmissionForm()
    return render(request, 'tickets/outsider_submission_form.html', {'form': form})

def submission_success_view(request):
    return render(request, 'tickets/submission_success.html')

# --- Ticket Status Views (No changes needed) ---
def check_status_view(request):
    return render(request, 'tickets/check_status.html')

def status_result_view(request):
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

# --- Ticket Download and Preview Views (No changes needed) ---
def download_ticket_view(request, submission_id):
    submission = get_object_or_404(Submission, id=submission_id, status='approved')
    pdf_buffer = generate_ticket_pdf(submission)
    response = HttpResponse(pdf_buffer, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="ticket_{submission.ticket_id}.pdf"'
    return response

def ticket_preview_image_view(request, submission_id):
    submission = get_object_or_404(Submission, id=submission_id, status='approved')
    pdf_buffer = generate_ticket_pdf(submission)
    images = convert_from_bytes(pdf_buffer.read(), first_page=1, last_page=1)
    image = images[0]
    img_buffer = BytesIO()
    image.save(img_buffer, 'PNG')
    img_buffer.seek(0)
    return HttpResponse(img_buffer, content_type='image/png')

# --- TICKET SCANNING AND VERIFICATION VIEWS ---
@login_required
def scan_ticket_view(request):
    return render(request, 'tickets/scan_ticket.html')

@csrf_exempt
@login_required
def verify_ticket_api(request):
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

            return JsonResponse({
                'status': 'success',
                'message': 'Valid Ticket Found!',
                'attendee': submission.full_name,
                'email': submission.email,
                'ticket_id': submission.ticket_id,
                'qr_code_id': submission.qr_code_id
            })
        except Submission.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Invalid Ticket Code'})
        except Exception:
            return JsonResponse({'status': 'error', 'message': 'An unexpected error occurred.'})
    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'}, status=405)

@csrf_exempt
@login_required
def confirm_check_in_api(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            qr_code_id = data.get('qr_code_id')
            submission = Submission.objects.get(qr_code_id=qr_code_id)
            
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


# --- KIOSK WORKFLOW VIEWS ---
# ---------------------------------

# View for the customer to fill out at the kiosk
def kiosk_request_view(request):
    if request.method == 'POST':
        form = KioskRequestForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('kiosk_request_success')
    else:
        form = KioskRequestForm()
    return render(request, 'tickets/kiosk_request_form.html', {'form': form})

# Success page after customer submits the kiosk form
def kiosk_request_success_view(request):
    return render(request, 'tickets/kiosk_request_success.html')

# Custom dashboard for kiosk staff
@login_required
def kiosk_staff_dashboard_view(request):
    one_minute_ago = timezone.now() - timedelta(minutes=1)
    requests = KioskRequest.objects.filter(
        assigned_to=request.user,
        created_at__gte=one_minute_ago
    )
    return render(request, 'tickets/kiosk_staff_dashboard.html', {'requests': requests})

# Logic to accept a request and create a pending submission
@login_required
def accept_kiosk_request_view(request, request_id):
    kiosk_request = get_object_or_404(KioskRequest, id=request_id, assigned_to=request.user)
    
    if Submission.objects.filter(email__iexact=kiosk_request.email).exists():
        messages.warning(request, f"A submission for '{kiosk_request.email}' already exists. The duplicate request has been deleted.")
        kiosk_request.delete()
        return redirect('kiosk_staff_dashboard')

    Submission.objects.create(
        full_name=kiosk_request.full_name,
        email=kiosk_request.email,
        attendee_type=kiosk_request.attendee_type,
        pass_type=kiosk_request.pass_type,
        transaction_id=f"KIOSK-CASH-({kiosk_request.cash_amount})-{request.user.username}",
        status='pending',
        processed_by=request.user
    )
    
    kiosk_request.delete()
    messages.success(request, f"Submission for '{kiosk_request.full_name}' has been successfully created.")
    return redirect('kiosk_staff_dashboard')

# Logic to reject/delete a kiosk request
@login_required
def reject_kiosk_request_view(request, request_id):
    kiosk_request = get_object_or_404(KioskRequest, id=request_id, assigned_to=request.user)
    kiosk_request.delete()
    messages.info(request, "The kiosk request has been deleted.")
    return redirect('kiosk_staff_dashboard')
