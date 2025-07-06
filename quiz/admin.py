from django.contrib import admin
from .models import Quiz

@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ['title', 'month', 'created_at']
    list_filter = ['month', 'created_at']
    search_fields = ['title', 'month']
    list_editable = ['month']
