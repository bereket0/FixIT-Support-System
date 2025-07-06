from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Quiz
from .forms import QuizForm

# Create your views here.

@login_required
def quiz_list(request):
    """List all quizzes with filtering and pagination"""
    quizzes = Quiz.objects.all()
    
    # Filtering
    month_filter = request.GET.get('month')
    search_query = request.GET.get('search')
    
    if month_filter:
        quizzes = quizzes.filter(month__icontains=month_filter)
    if search_query:
        quizzes = quizzes.filter(
            Q(title__icontains=search_query) | 
            Q(month__icontains=search_query)
        )
    
    # Pagination
    paginator = Paginator(quizzes, 6)  # 6 quizzes per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'current_filters': {
            'month': month_filter,
            'search': search_query,
        }
    }
    
    return render(request, 'quiz/quiz_list.html', context)

@login_required
def quiz_create(request):
    """Create a new quiz (IT Admin only)"""
    if not request.user.groups.filter(name='IT Admin').exists():
        messages.error(request, 'Only IT Admins can create quizzes.')
        return redirect('quiz_list')
    
    if request.method == 'POST':
        form = QuizForm(request.POST)
        if form.is_valid():
            quiz = form.save()
            messages.success(request, 'Quiz created successfully!')
            return redirect('quiz_detail', pk=quiz.pk)
    else:
        form = QuizForm()
    
    return render(request, 'quiz/quiz_form.html', {
        'form': form,
        'action': 'Create'
    })

@login_required
def quiz_detail(request, pk):
    """View quiz details"""
    quiz = get_object_or_404(Quiz, pk=pk)
    is_admin = request.user.groups.filter(name='IT Admin').exists()
    
    return render(request, 'quiz/quiz_detail.html', {
        'quiz': quiz,
        'is_admin': is_admin
    })

@login_required
def quiz_edit(request, pk):
    """Edit a quiz (IT Admin only)"""
    quiz = get_object_or_404(Quiz, pk=pk)
    
    if not request.user.groups.filter(name='IT Admin').exists():
        messages.error(request, 'Only IT Admins can edit quizzes.')
        return redirect('quiz_detail', pk=quiz.pk)
    
    if request.method == 'POST':
        form = QuizForm(request.POST, instance=quiz)
        if form.is_valid():
            form.save()
            messages.success(request, 'Quiz updated successfully!')
            return redirect('quiz_detail', pk=quiz.pk)
    else:
        form = QuizForm(instance=quiz)
    
    return render(request, 'quiz/quiz_form.html', {
        'form': form,
        'quiz': quiz,
        'action': 'Edit'
    })

@login_required
def quiz_delete(request, pk):
    """Delete a quiz (IT Admin only)"""
    quiz = get_object_or_404(Quiz, pk=pk)
    
    if not request.user.groups.filter(name='IT Admin').exists():
        messages.error(request, 'Only IT Admins can delete quizzes.')
        return redirect('quiz_detail', pk=quiz.pk)
    
    if request.method == 'POST':
        quiz.delete()
        messages.success(request, 'Quiz deleted successfully!')
        return redirect('quiz_list')
    
    return render(request, 'quiz/quiz_confirm_delete.html', {
        'quiz': quiz
    })
