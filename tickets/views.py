from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Submission
from .forms import SubmissionForm
from .pdf_utils import generate_ticket_pdf
from pdf2image import convert_from_bytes # Import the new library
from io import BytesIO

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

# --- Ticket Download and Preview Views ---
def download_ticket_view(request, submission_id):
    submission = get_object_or_404(Submission, id=submission_id, status='approved')
    pdf_buffer = generate_ticket_pdf(submission)
    response = HttpResponse(pdf_buffer, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="ticket_{submission.ticket_id}.pdf"'
    return response

# --- NEW: Ticket Preview View ---
def ticket_preview_image_view(request, submission_id):
    """
    Generates a PNG image preview of the ticket.
    """
    submission = get_object_or_404(Submission, id=submission_id, status='approved')
    pdf_buffer = generate_ticket_pdf(submission)

    # Convert the first page of the PDF to an image
    images = convert_from_bytes(pdf_buffer.read(), first_page=1, last_page=1)
    image = images[0]

    # Save the image to a memory buffer
    img_buffer = BytesIO()
    image.save(img_buffer, 'PNG')
    img_buffer.seek(0)

    return HttpResponse(img_buffer, content_type='image/png')


# --- Admin Facing Views ---
# (These views remain the same)
def admin_dashboard_view(request):
    submissions = Submission.objects.all()
    return render(request, 'tickets/admin_dashboard.html', {'submissions': submissions})

def approve_submission_view(request, submission_id):
    submission = get_object_or_404(Submission, id=submission_id)
    # This logic is now handled by the Django Admin action
    submission.status = 'approved'
    submission.save()
    return redirect('admin_dashboard')

def reject_submission_view(request, submission_id):
    submission = get_object_or_404(Submission, id=submission_id)
    submission.status = 'rejected'
    submission.save()
    return redirect('admin_dashboard')