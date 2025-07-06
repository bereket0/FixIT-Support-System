from django.urls import path
from . import views

urlpatterns = [
    path('', views.tip_list, name='tip_list'),
    path('create/', views.tip_create, name='tip_create'),
    path('<int:pk>/', views.tip_detail, name='tip_detail'),
    path('<int:pk>/edit/', views.tip_edit, name='tip_edit'),
    path('<int:pk>/delete/', views.tip_delete, name='tip_delete'),
] 