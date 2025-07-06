from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.db.models import Q
from django.utils import timezone
from .models import Ticket
from .forms import TicketForm, TicketAdminForm

# Create your views here.

@login_required
def ticket_list(request):
    """List all tickets with filtering and pagination"""
    is_admin = request.user.groups.filter(name='IT Admin').exists()
    
    # Get tickets based on user role
    if is_admin:
        tickets = Ticket.objects.all()
    else:
        tickets = Ticket.objects.filter(created_by=request.user)
    
    # Filtering
    status_filter = request.GET.get('status', '')
    category_filter = request.GET.get('category', '')
    search_query = request.GET.get('search', '').strip()
    
    if status_filter and status_filter != 'None':
        tickets = tickets.filter(status=status_filter)
    if category_filter and category_filter != 'None':
        tickets = tickets.filter(category=category_filter)
    if search_query and search_query != 'None':
        tickets = tickets.filter(
            Q(subject__icontains=search_query) | 
            Q(description__icontains=search_query)
        )
    
    # Pagination
    paginator = Paginator(tickets, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'is_admin': is_admin,
        'status_choices': Ticket.STATUS_CHOICES,
        'category_choices': Ticket.CATEGORY_CHOICES,
        'current_filters': {
            'status': status_filter if status_filter != 'None' else '',
            'category': category_filter if category_filter != 'None' else '',
            'search': search_query if search_query != 'None' else '',
        }
    }
    
    return render(request, 'tickets/ticket_list.html', context)

@login_required
def ticket_create(request):
    """Create a new ticket"""
    if request.method == 'POST':
        form = TicketForm(request.POST, request.FILES)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.created_by = request.user
            ticket.save()
            messages.success(request, 'Ticket created successfully!')
            return redirect('ticket_detail', pk=ticket.pk)
    else:
        form = TicketForm()
    
    return render(request, 'tickets/ticket_form.html', {
        'form': form,
        'action': 'Create',
        'is_admin': request.user.groups.filter(name='IT Admin').exists()
    })

@login_required
def ticket_detail(request, pk):
    """View ticket details"""
    ticket = get_object_or_404(Ticket, pk=pk)
    is_admin = request.user.groups.filter(name='IT Admin').exists()
    
    # Check if user has permission to view this ticket
    if not is_admin and ticket.created_by != request.user:
        messages.error(request, 'You do not have permission to view this ticket.')
        return redirect('ticket_list')
    
    return render(request, 'tickets/ticket_detail.html', {
        'ticket': ticket,
        'is_admin': is_admin
    })

@login_required
def ticket_edit(request, pk):
    """Edit a ticket"""
    ticket = get_object_or_404(Ticket, pk=pk)
    is_admin = request.user.groups.filter(name='IT Admin').exists()
    
    # Check permissions
    if not is_admin and ticket.created_by != request.user:
        messages.error(request, 'You do not have permission to edit this ticket.')
        return redirect('ticket_list')
    
    if request.method == 'POST':
        if is_admin:
            form = TicketAdminForm(request.POST, request.FILES, instance=ticket)
        else:
            form = TicketForm(request.POST, request.FILES, instance=ticket)
        
        if form.is_valid():
            # Track who made the changes
            ticket.last_modified_by = request.user
            
            # If employee is making changes, track the update and preserve status
            if not is_admin:
                ticket.last_employee_update = timezone.now()
                # Preserve the original status - employees cannot change it
                original_status = ticket.status
                
                # Save the form
                form.save()
                
                # Ensure status wasn't changed by employee
                ticket.refresh_from_db()
                if ticket.status != original_status:
                    ticket.status = original_status
                    ticket.save(update_fields=['status'])
                
                # Set employee notes
                employee_notes = form.cleaned_data.get('employee_update_notes', '')
                if employee_notes:
                    ticket.employee_update_notes = employee_notes
                    ticket.save(update_fields=['employee_update_notes'])
            else:
                # Admin can change status normally
                form.save()
            
            messages.success(request, 'Ticket updated successfully!')
            return redirect('ticket_detail', pk=ticket.pk)
    else:
        if is_admin:
            form = TicketAdminForm(instance=ticket)
        else:
            form = TicketForm(instance=ticket)
    
    return render(request, 'tickets/ticket_form.html', {
        'form': form,
        'ticket': ticket,
        'action': 'Edit',
        'is_admin': is_admin
    })

@login_required
def ticket_delete(request, pk):
    """Delete a ticket"""
    ticket = get_object_or_404(Ticket, pk=pk)
    is_admin = request.user.groups.filter(name='IT Admin').exists()
    
    # Check permissions
    if not is_admin and ticket.created_by != request.user:
        messages.error(request, 'You do not have permission to delete this ticket.')
        return redirect('ticket_list')
    
    if request.method == 'POST':
        ticket.delete()
        messages.success(request, 'Ticket deleted successfully!')
        return redirect('ticket_list')
    
    return render(request, 'tickets/ticket_confirm_delete.html', {
        'ticket': ticket,
        'is_admin': is_admin
    })
