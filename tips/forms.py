from django import forms
from .models import TechTip

class TechTipForm(forms.ModelForm):
    class Meta:
        model = TechTip
        fields = ['title', 'description', 'week_number', 'category']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter tip title'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 6, 'placeholder': 'Describe the tech tip in detail'}),
            'week_number': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'e.g., 1, 2, 3...'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
        }
        
    def clean_week_number(self):
        week_number = self.cleaned_data.get('week_number')
        if week_number < 1 or week_number > 52:
            raise forms.ValidationError('Week number must be between 1 and 52.')
        return week_number 