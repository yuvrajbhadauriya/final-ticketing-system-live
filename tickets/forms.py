from django import forms
from .models import Submission

class SubmissionForm(forms.ModelForm):
    """
    A form for creating new Submission objects.
    """
    class Meta:
        model = Submission
        fields = ['full_name', 'email', 'transaction_id', 'screenshot']