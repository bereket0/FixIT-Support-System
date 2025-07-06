from django.db import models
from django.contrib.auth.models import User

class Ticket(models.Model):
    CATEGORY_CHOICES = [
        ('Hardware', 'Hardware'),
        ('Software', 'Software'),
        ('Network', 'Network'),
        ('Other', 'Other'),
    ]
    
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('In Progress', 'In Progress'),
        ('Solved', 'Solved'),
    ]
    
    subject = models.CharField(max_length=200)
    description = models.TextField()
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    attachment = models.FileField(upload_to='tickets/', blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_tickets')
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_tickets')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Change tracking fields
    last_modified_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='modified_tickets')
    last_employee_update = models.DateTimeField(null=True, blank=True)
    employee_update_notes = models.TextField(blank=True, help_text="Notes about changes made by employee")
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.subject} - {self.status}"
