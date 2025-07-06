from django.db import models

# Create your models here.

class Quiz(models.Model):
    title = models.CharField(max_length=200)
    form_url = models.URLField()
    month = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = "Quizzes"
    
    def __str__(self):
        return f"{self.month}: {self.title}"
