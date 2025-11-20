from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('home/', views.home, name='home'),
    path('login/', views.login, name='login'),
    path('contact/', views.contact, name='contact'),
    path('about/', views.about, name='about'),
    path('info/', views.info, name='info'),
    path('signup/',views.signup,name='signup'),
    path('dashboard/',views.dashboard,name='dashboard'),
    path('attendance/',views.attendance,name='attendance'),
    path('employee/',views.employee,name='employee'),
    path('authendication/', views.authendication, name='authendication'),
path("student_home/", views.student_home, name="student_home"),
    path("save_student_details/", views.save_student_details, name="save_student_details"),
    path("student_profile/", views.student_profile, name="student_profile"),
path('logout/', views.logout, name='logout'),
path('teacher-management/', views.teacher_management, name='teacher_management'),
    path("checkregistration/", views.checkregistration, name="checkregistration"),
    path('admin/', admin.site.urls),
]