from django.urls import path
from . import views

urlpatterns = [
    path('', views.quiz_list, name='quiz_list'),
    path('create/', views.quiz_create, name='quiz_create'),
    path('<int:pk>/', views.quiz_detail, name='quiz_detail'),
    path('<int:pk>/edit/', views.quiz_edit, name='quiz_edit'),
    path('<int:pk>/delete/', views.quiz_delete, name='quiz_delete'),
] 