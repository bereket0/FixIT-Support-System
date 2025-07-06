from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from .models import TechTip
from .forms import TechTipForm

@login_required
def tip_list(request):
    """List all tech tips with filtering and pagination"""
    tips = TechTip.objects.all()
    
    # Filtering
    category_filter = request.GET.get('category')
    week_filter = request.GET.get('week')
    search_query = request.GET.get('search')
    
    if category_filter:
        tips = tips.filter(category=category_filter)
    if week_filter:
        tips = tips.filter(week_number=week_filter)
    if search_query:
        tips = tips.filter(
            Q(title__icontains=search_query) | 
            Q(description__icontains=search_query)
        )
    
    # Pagination
    paginator = Paginator(tips, 9)  # 9 tips per page for 3x3 grid
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'category_choices': TechTip.CATEGORY_CHOICES,
        'current_filters': {
            'category': category_filter,
            'week': week_filter,
            'search': search_query,
        }
    }
    
    return render(request, 'tips/tip_list.html', context)

@login_required
def tip_create(request):
    """Create a new tech tip (IT Admin only)"""
    if not request.user.groups.filter(name='IT Admin').exists():
        messages.error(request, 'Only IT Admins can create tech tips.')
        return redirect('tip_list')
    
    if request.method == 'POST':
        form = TechTipForm(request.POST)
        if form.is_valid():
            tip = form.save()
            messages.success(request, 'Tech tip created successfully!')
            return redirect('tip_detail', pk=tip.pk)
    else:
        form = TechTipForm()
    
    return render(request, 'tips/tip_form.html', {
        'form': form,
        'action': 'Create'
    })

@login_required
def tip_detail(request, pk):
    """View tech tip details"""
    tip = get_object_or_404(TechTip, pk=pk)
    is_admin = request.user.groups.filter(name='IT Admin').exists()
    
    return render(request, 'tips/tip_detail.html', {
        'tip': tip,
        'is_admin': is_admin
    })

@login_required
def tip_edit(request, pk):
    """Edit a tech tip (IT Admin only)"""
    tip = get_object_or_404(TechTip, pk=pk)
    
    if not request.user.groups.filter(name='IT Admin').exists():
        messages.error(request, 'Only IT Admins can edit tech tips.')
        return redirect('tip_detail', pk=tip.pk)
    
    if request.method == 'POST':
        form = TechTipForm(request.POST, instance=tip)
        if form.is_valid():
            form.save()
            messages.success(request, 'Tech tip updated successfully!')
            return redirect('tip_detail', pk=tip.pk)
    else:
        form = TechTipForm(instance=tip)
    
    return render(request, 'tips/tip_form.html', {
        'form': form,
        'tip': tip,
        'action': 'Edit'
    })

@login_required
def tip_delete(request, pk):
    """Delete a tech tip (IT Admin only)"""
    tip = get_object_or_404(TechTip, pk=pk)
    
    if not request.user.groups.filter(name='IT Admin').exists():
        messages.error(request, 'Only IT Admins can delete tech tips.')
        return redirect('tip_detail', pk=tip.pk)
    
    if request.method == 'POST':
        tip.delete()
        messages.success(request, 'Tech tip deleted successfully!')
        return redirect('tip_list')
    
    return render(request, 'tips/tip_confirm_delete.html', {
        'tip': tip
    })
