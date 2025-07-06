from django import forms
from .models import Ticket
from django.contrib.auth.models import User

class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['subject', 'description', 'category', 'attachment', 'employee_update_notes']
        widgets = {
            'subject': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter ticket subject'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Describe your issue in detail'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'attachment': forms.FileInput(attrs={'class': 'form-control'}),
            'employee_update_notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Add any notes about your changes (optional)'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Explicitly exclude status and assigned_to fields for employees
        if 'status' in self.fields:
            del self.fields['status']
        if 'assigned_to' in self.fields:
            del self.fields['assigned_to']

class TicketAdminForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['subject', 'description', 'category', 'status', 'assigned_to', 'attachment']
        widgets = {
            'subject': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'assigned_to': forms.Select(attrs={'class': 'form-control'}),
            'attachment': forms.FileInput(attrs={'class': 'form-control'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Only show IT Admin users in the assigned_to field
        it_admin_users = User.objects.filter(groups__name='IT Admin')
        self.fields['assigned_to'].queryset = it_admin_users 