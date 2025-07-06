from django.db import models

# Create your models here.

class TechTip(models.Model):
    CATEGORY_CHOICES = [
        ('Word', 'Word'),
        ('Outlook', 'Outlook'),
        ('Shortcut', 'Shortcut'),
        ('Other', 'Other'),
    ]
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    week_number = models.IntegerField()
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-week_number', '-created_at']
    
    def __str__(self):
        return f"Week {self.week_number}: {self.title}"
