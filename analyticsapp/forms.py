from django import forms
from .models import CSVfile

class CsvForm(forms.ModelForm):
    class Meta:
        model=CSVfile
        fields=['file']