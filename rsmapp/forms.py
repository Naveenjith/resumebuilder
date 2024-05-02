from django import forms
from .models import Resume

class ResumeForm(forms.ModelForm):
    class Meta:
        model = Resume
        fields = ['fname','lname','role','dob','email','address','profile','skills','education','experience','image']
        widgets = {
            'dob': forms.DateInput(attrs={'type': 'date'})
        }

    