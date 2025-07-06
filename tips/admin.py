from django.contrib import admin
from .models import TechTip

@admin.register(TechTip)
class TechTipAdmin(admin.ModelAdmin):
    list_display = ['title', 'week_number', 'category', 'created_at']
    list_filter = ['category', 'week_number', 'created_at']
    search_fields = ['title', 'description']
    list_editable = ['week_number', 'category']
