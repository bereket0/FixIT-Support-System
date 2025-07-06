from django.contrib import admin
from .models import Ticket

@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ['subject', 'category', 'status', 'created_by', 'assigned_to', 'created_at']
    list_filter = ['status', 'category', 'created_at']
    search_fields = ['subject', 'description', 'created_by__username']
    list_editable = ['status', 'assigned_to']
    readonly_fields = ['created_at', 'updated_at']
