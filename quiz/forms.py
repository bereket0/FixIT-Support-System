from django import forms
from .models import Quiz

class QuizForm(forms.ModelForm):
    class Meta:
        model = Quiz
        fields = ['title', 'form_url', 'month']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter quiz title'}),
            'form_url': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://forms.google.com/...'}),
            'month': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., January 2024, February 2024'}),
        }
        
    def clean_form_url(self):
        form_url = self.cleaned_data.get('form_url')
        if not form_url.startswith(('http://', 'https://')):
            raise forms.ValidationError('Please enter a valid URL starting with http:// or https://')
        return form_url 