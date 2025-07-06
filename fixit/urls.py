"""
URL configuration for fixit project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from users import views as user_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', user_views.employee_dashboard, name='employee_dashboard'),  # Public employee dashboard
    path('admin-dashboard/', user_views.admin_dashboard, name='admin_dashboard'),  # Admin dashboard (login required)
    path('login/', user_views.login_view, name='login'),  # Custom login
    path('logout/', user_views.logout_view, name='logout'),  # Custom logout
    path('create-employee/', user_views.create_employee, name='create_employee'),  # Create employee account
    path('tickets/', include('tickets.urls')),
    path('tips/', include('tips.urls')),
    path('quiz/', include('quiz.urls')),
]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# Custom error handlers
handler404 = 'users.views.custom_404'
handler500 = 'users.views.custom_500'
