"""
URL configuration for school_management_project project.

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
from django.urls import path
from school_app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('admin_page/', views.admin_page , name='admin_page'),
    path('log_out/', views.log_out , name='log_out'),
    path('', views.home_page , name='home_page'),
    path('login_page/', views.login_page , name='login_page'),
    path('register_department/', views.register_department , name='register_department'),
    path('delete_department/<int:id>/', views.delete_department , name='delete_department'),
    path('register_student/', views.register_student , name='register_student'),
    path('register_teacher/', views.register_teacher , name='register_teacher'),
    path('admin_student_view/', views.admin_student_view , name='admin_student_view'),
    path('admin_teacher_view/', views.admin_teacher_view , name='admin_teacher_view'),
    path('student_profile/', views.student_profile , name='student_profile'),
    path('student_profile_edit/', views.student_profile_edit, name='student_profile_edit'),
    path('teacher_profile/', views.teacher_profile, name='teacher_profile'),
    path('teacher_profile_edit/', views.teacher_profile_edit, name='teacher_profile_edit'),
]
