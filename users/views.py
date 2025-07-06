from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import Group, User
from django.contrib import messages
from django.http import JsonResponse, Http404
from django.views.decorators.http import require_http_methods
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from django.db.models import Count, Q
from datetime import datetime, timedelta
from tickets.models import Ticket
from tips.models import TechTip
from quiz.models import Quiz

def is_admin(user):
    return user.is_authenticated and user.groups.filter(name='IT Admin').exists()

def custom_404(request, exception):
    """Custom 404 error handler"""
    return render(request, 'users/404.html', status=404)

def custom_500(request):
    """Custom 500 error handler"""
    return render(request, 'users/500.html', status=500)

def employee_dashboard(request):
    """Public employee dashboard - no login required"""
    context = {
        'recent_tips': TechTip.objects.all().order_by('-created_at')[:4],
        'current_quiz': Quiz.objects.all().order_by('-created_at').first(),
    }
    
    # Add user-specific data if logged in
    if request.user.is_authenticated:
        context['user_tickets'] = Ticket.objects.filter(created_by=request.user).order_by('-created_at')[:3]
    
    return render(request, 'users/employee_dashboard.html', context)

@login_required
@user_passes_test(is_admin)
def admin_dashboard(request):
    """Admin dashboard with comprehensive statistics"""
    # Get ticket statistics
    total_tickets = Ticket.objects.count()
    pending_tickets = Ticket.objects.filter(status='Pending').count()
    in_progress_tickets = Ticket.objects.filter(status='In Progress').count()
    solved_tickets = Ticket.objects.filter(status='Solved').count()
    
    # Monthly statistics
    current_month = datetime.now().month
    current_year = datetime.now().year
    
    monthly_stats = {
        'new_tickets': Ticket.objects.filter(
            created_at__month=current_month,
            created_at__year=current_year
        ).count(),
        'solved_tickets': Ticket.objects.filter(
            status='Solved',
            updated_at__month=current_month,
            updated_at__year=current_year
        ).count(),
    }
    
    # Recent activity
    recent_tickets = Ticket.objects.select_related('created_by').order_by('-created_at')[:5]
    recent_tips = TechTip.objects.order_by('-created_at')[:3]
    
    # Get recent employee accounts
    employee_group = Group.objects.get(name='Employee')
    recent_employees = User.objects.filter(groups=employee_group).order_by('-date_joined')[:5]
    
    context = {
        'total_tickets': total_tickets,
        'pending_tickets': pending_tickets,
        'in_progress_tickets': in_progress_tickets,
        'solved_tickets': solved_tickets,
        'monthly_stats': monthly_stats,
        'recent_tickets': recent_tickets,
        'recent_tips': recent_tips,
        'recent_employees': recent_employees,
    }
    
    return render(request, 'users/admin_dashboard.html', context)

@login_required
@user_passes_test(is_admin)
def create_employee(request):
    """Create a new employee account"""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        email = request.POST.get('email', '')
        
        # Validation
        if not username or not password:
            messages.error(request, 'Username and password are required.')
            return redirect('admin_dashboard')
        
        if password != confirm_password:
            messages.error(request, 'Passwords do not match.')
            return redirect('admin_dashboard')
        
        if len(password) < 8:
            messages.error(request, 'Password must be at least 8 characters long.')
            return redirect('admin_dashboard')
        
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists.')
            return redirect('admin_dashboard')
        
        try:
            # Create user
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                first_name=request.POST.get('first_name', ''),
                last_name=request.POST.get('last_name', '')
            )
            
            # Add to Employee group
            employee_group = Group.objects.get(name='Employee')
            user.groups.add(employee_group)
            
            messages.success(request, f'Employee account "{username}" created successfully!')
            return redirect('admin_dashboard')
            
        except Exception as e:
            messages.error(request, f'Error creating employee account: {str(e)}')
            return redirect('admin_dashboard')
    
    return redirect('admin_dashboard')

def login_view(request):
    """Custom login view"""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            # Redirect to admin dashboard if user is admin, otherwise employee dashboard
            if user.groups.filter(name='IT Admin').exists():
                return redirect('admin_dashboard')
            else:
                return redirect('employee_dashboard')
        else:
            messages.error(request, 'Invalid username or password.')
    
    return render(request, 'users/login.html')

def logout_view(request):
    """Custom logout view with thank you message"""
    return render(request, 'users/logout.html')
