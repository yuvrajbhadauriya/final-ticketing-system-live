from django import forms
from .models import Submission

class VipsSubmissionForm(forms.ModelForm):
    """
    A dedicated form for VIPS Student submissions.
    This form includes the required VIPS ID card upload.
    """
    class Meta:
        model = Submission
        # --- ADD 'pass_type' to the fields list ---
        fields = ['full_name', 'email', 'pass_type', 'transaction_id', 'vips_id_card', 'screenshot']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make these fields required on the public form
        self.fields['vips_id_card'].required = True
        self.fields['screenshot'].required = True

class OutsiderSubmissionForm(forms.ModelForm):
    """
    A dedicated form for Outsider submissions.
    This form does NOT include the VIPS ID card field.
    """
    class Meta:
        model = Submission
        # --- ADD 'pass_type' to the fields list ---
        fields = ['full_name', 'email', 'pass_type', 'transaction_id', 'screenshot']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make this field required on the public form
        self.fields['screenshot'].required = True
