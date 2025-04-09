from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from myapp import views
from .views import custom_report, leave_trends, employee_productivity
urlpatterns = [

    path('', views.login_view, name='login'),  
    path('register/', views.register, name='register'),  # HR & Managers only
    path('logout/', views.logout_view, name='logout_view'),

    path('dashboard/', views.dashboard, name='dashboard'),
    path('home/', views.home, name='home'),

    path('employees/', views.employee_list, name='employee_list'),
    path("employees/<int:emp_id>/", views.employee_profile, name="employee_profile"),
    path('employees/add/', views.add_employee, name='add_employee'),  
    path("employees/edit/<int:emp_id>/", views.edit_employee, name="edit_employee"),
    path('delete_employee/<int:employee_id>/', views.delete_employee, name='delete_employee'),

    path('projects/', views.project_dashboard, name='project_dashboard'),
    path('projects/<int:project_id>/', views.project_details, name='project_details'),
    path('projects/add/', views.add_project, name='add_project'),
    path('projects/edit/<int:project_id>/', views.edit_project, name='edit_project'),
    path('projects/<int:project_id>/add_task/', views.add_task, name='add_task'),
    path('projects/<int:project_id>/delete/', views.delete_project, name='delete_project'),
    path('tasks/<int:task_id>/edit/', views.edit_task, name='edit_task'),  # Add this line
    path('tasks/<int:task_id>/mark_completed/', views.mark_task_completed, name='mark_task_completed'),
    path('projects/<int:project_id>/mark_completed/', views.mark_project_completed, name='mark_project_completed'),
    path('projects/dashboard/', views.project_dashboard, name='project_dashboard'),
    path('login_redirect/', views.login_redirect_view, name='login_redirect'),


    path('leave/request/', views.leave_request_view, name='leave_request'),
    path('leave/history/', views.leave_history_view, name='leave_history'),
    path('leave/approval/', views.leave_approval_view, name='leave_approval'),
    path('leave/approve/<int:leave_id>/', views.approve_leave, name='approve_leave'),
    path('leave/reject/<int:leave_id>/', views.reject_leave, name='reject_leave'),

    path('performance/', views.performance_dashboard, name='performance_dashboard'),
    path('leave-trends/', views.leave_trends, name='leave_trends'),
    path('productivity/', views.employee_productivity, name='employee_productivity'),
    path('generate-report/', views.generate_report, name='generate_report'),
    path('custom_report/', views.custom_report, name='custom_report'),

    path('notifications/', views.notifications_view, name='notifications_list'),
    path('messages/inbox/', views.inbox_view, name='messages_inbox'),
    path('communication/', views.communication_view, name='communication_tools'),
    path('announcements/', views.announcements_view, name='announcement_list'),

    path('custom_report/', views.custom_report, name='custom_report'),
    path('leave-trends/', views.leave_trends, name='leave_trends'),
    path('productivity/', views.employee_productivity, name='employee_productivity'),


    path('performance/custom_report/', custom_report, name='custom_report'),
    path('performance/leave-trends/', leave_trends, name='leave_trends'),
    path('performance/productivity/', employee_productivity, name='employee_productivity'),

]
