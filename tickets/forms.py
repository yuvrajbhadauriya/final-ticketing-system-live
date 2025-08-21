from django import forms
from .models import Submission, KioskRequest
from django.contrib.auth.models import User

class VipsSubmissionForm(forms.ModelForm):
    class Meta:
        model = Submission
        fields = ['full_name', 'email', 'pass_type', 'transaction_id', 'vips_id_card', 'screenshot']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['vips_id_card'].required = True
        self.fields['screenshot'].required = True

class OutsiderSubmissionForm(forms.ModelForm):
    class Meta:
        model = Submission
        fields = ['full_name', 'email', 'pass_type', 'transaction_id', 'screenshot']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['screenshot'].required = True

class KioskRequestForm(forms.ModelForm):
    class Meta:
        model = KioskRequest
        fields = ['full_name', 'email', 'attendee_type', 'pass_type', 'cash_amount', 'assigned_to']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # --- THIS IS THE FIX ---
        # Only show users who are in the "Kiosk Team" group
        self.fields['assigned_to'].queryset = User.objects.filter(groups__name='Kiosk Team')
        self.fields['assigned_to'].label = "Kiosk Team Member"