from .models import Employee
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseForbidden
from myapp.models import Employee, Project
from .decorators import role_required
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from myapp.models import Employee
from .decorators import role_required
from django.utils.crypto import get_random_string  # Generates random passwords
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Notification, Message, Announcement
from .forms import MessageForm, AnnouncementForm,NotificationForm
from django.contrib.auth.decorators import login_required
from .decorators import role_required
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Task, Project, Employee
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from myapp.models import Task  # Update with your app name
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from myapp.models import Employee
from myapp.decorators import role_required
from django.contrib.auth import get_user_model
from django.utils.crypto import get_random_string  # Generates random passwords
from django.shortcuts import get_object_or_404
from .models import Employee
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Project, Task, Employee
from django.shortcuts import redirect
from django.http import JsonResponse
from django.shortcuts import render
from django.urls import reverse  # Import reverse for redirecting
from .models import Project, Employee  # Import models
from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from django.contrib.auth import logout
from django.contrib.auth.models import Group
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Notification
from .forms import NotificationForm
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from myapp.models import Employee, Project, LeaveRequest, Notification, Announcement
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import Employee, Project, LeaveRequest, Notification, Announcement
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from myapp.models import Employee, Project, LeaveRequest, Notification, Announcement
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from myapp.models import Employee, Project, LeaveRequest, Notification, Announcement
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Notification
from .forms import NotificationForm
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model, authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt



def register(request):
    User = get_user_model()
    
    # Check if there is at least one HR or Manager in the system
    hr_exists = User.objects.filter(role="hr").exists()
    manager_exists = User.objects.filter(role="manager").exists()

    # If there are HR or Managers, restrict access to only logged-in HR/Managers
    if hr_exists or manager_exists:
        if not request.user.is_authenticated or request.user.role not in ["hr", "manager"]:
            messages.error(request, "Access Denied!")
            return redirect("login")  # Redirect employees to login
    
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")
        role = request.POST.get("role")  # Get role from the form

        if not username or not email or not password1 or not password2 or not role:
            messages.error(request, "All fields are required!")
            return redirect("register")

        if password1 != password2:
            messages.error(request, "Passwords do not match")
            return redirect("register")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect("register")

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered")
            return redirect("register")

        # Ensure only HR & Managers can be created from this form
        if role not in ["hr", "manager"]:
            messages.error(request, "Invalid role selection!")
            return redirect("register")

        # Create User
        user = User.objects.create_user(username=username, email=email, password=password1, role=role)
        user.save()

        messages.success(request, "Registration successful! Please login.")
        return redirect("login")

    return render(request, "register.html")


def login_view(request):
    if request.user.is_authenticated:  # If user is already logged in
        return redirect("dashboard")  # Redirect to dashboard

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, "Login successful!")
            return redirect("dashboard")  # Redirect to dashboard

        else:
            messages.error(request, "Invalid username or password")
            return redirect("login")

    return render(request, "login.html")

from django.contrib.auth import logout
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt  # Allow AJAX requests
def logout_view(request):
    if request.method == "POST":
        logout(request)
        return redirect("login")  # Redirect to login page after logout
    



from django.shortcuts import redirect

def login_redirect_view(request):
    user = request.user  # Get logged-in user

    if user.is_authenticated:
        return redirect('dashboard')  # Redirect everyone to the same dashboard
    else:
        return redirect('login')  # If not logged in, go to login page



@login_required
def dashboard(request):
    user = request.user

    # **Check if the User is an Employee, HR, or Manager**
    try:
        employee_instance = Employee.objects.get(user=user)  # Convert `User` to `Employee`
    except Employee.DoesNotExist:
        employee_instance = None  # If the user is not an employee

    # **Determine Role Correctly**
    if user.is_superuser:
        role = "Admin"
    elif employee_instance:
        role = employee_instance.role  # Use stored role from Employee model
    else:
        messages.error(request, "You do not have a valid role assigned. Contact Admin.")
        return redirect("login")

    # **Fetch Data Based on Role**
    employee_count = Employee.objects.count() if role in ["Admin", "HR"] else None
    active_project_count = Project.objects.filter(status__in=["Active", "On Hold"]).count()
    pending_leaves = LeaveRequest.objects.filter(status="Pending").count() if role in ["Admin", "HR"] else None

    # **Fix Assigned Projects Query**
    assigned_projects = None
    if role in ["Employee", "Manager"] and employee_instance:
        assigned_projects = Project.objects.filter(assigned_to=employee_instance)

    # **Fetch Notifications & Announcements**
    notifications = Notification.objects.all().order_by('-created_at')[:5]
    announcements = Announcement.objects.all().order_by('-created_at')[:5]

    # **Pass Data to Template**
    context = {
        "username": user.username,
        "role": role,  # Now correctly fetched from Employee model
        "employee_count": employee_count,
        "active_project_count": active_project_count,
        "pending_leaves": pending_leaves,
        "notifications": notifications,
        "announcements": announcements,
        "assigned_projects": assigned_projects,
    }

    return render(request, "dashboard.html", context)


@login_required
def employee_list(request):
    search_query = request.GET.get("search", "")
    employees = Employee.objects.filter(name__icontains=search_query)
    
    return render(request, "employee_list.html", {"employees": employees, "search_query": search_query})


@login_required
def employee_profile(request, emp_id):
    employee = get_object_or_404(Employee, id=emp_id)
    return render(request, "employee_profile.html", {"employee": employee})



CustomUser = get_user_model()  # Get the CustomUser model dynamically

@login_required
@role_required(["Admin", "HR"])  # Only Admin & HR can add employees
def add_employee(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        designation = request.POST.get("designation")
        salary = request.POST.get("salary")
        department = request.POST.get("department")  # Debug this line
        role = request.POST.get("role")
        role = request.POST.get("role").lower()  # Store role in lowercase

        username = request.POST.get("username")  

        print("Department received from form:", department)  # Debug print

        # Check if Username Already Exists
        if CustomUser.objects.filter(username=username).exists():
            messages.error(request, f"Username '{username}' is already taken. Choose another one.")
            return redirect("add_employee")

        # Check if Email Already Exists (Optional)
        if CustomUser.objects.filter(email=email).exists():
            messages.error(request, f"Email '{email}' is already in use.")
            return redirect("add_employee")

        # Generate a random password if not provided
        password = request.POST.get("password") or get_random_string(8)

        # Create User using CustomUser model
        user = CustomUser.objects.create_user(username=username, email=email, password=password)

        # Assign the correct group based on the role
        group_name = role.capitalize()
        group, created = Group.objects.get_or_create(name=group_name)
        user.groups.add(group)
        user.save()

        # Create Employee Profile
        employee = Employee.objects.create(
            user=user,
            name=name,
            email=email,
            phone=phone,
            designation=designation,
            salary=salary,
            department=department,  # This should store 'Testing' if selected
            role=role.lower()
        )

        print("Employee saved with department:", employee.department)  # Debug print

        messages.success(request, f"Employee {name} added successfully! Username: {username}, Password: {password}")

        return redirect("employee_list")  

    return render(request, "add_employee.html")




@login_required
@role_required(["Admin", "HR"])  # Only Admin and HR can edit employee details
def edit_employee(request, emp_id):
    employee = get_object_or_404(Employee, id=emp_id)
    user = employee.user  # Get associated User object

    if request.method == "POST":
        new_username = request.POST.get("username")
        new_email = request.POST.get("email")

        # **Check if Username Already Exists (excluding current user)**
        if CustomUser.objects.filter(username=new_username).exclude(id=user.id).exists():
            messages.error(request, "Username already taken. Choose another one.")
            return redirect("edit_employee", emp_id=emp_id)

        # **Check if Email Already Exists (excluding current user)**
        if CustomUser.objects.filter(email=new_email).exclude(id=user.id).exists():
            messages.error(request, "Email already in use.")
            return redirect("edit_employee", emp_id=emp_id)

        # **Update User model**
        user.username = new_username
        user.email = new_email
        user.save()

        # **Update Employee model**
        employee.name = request.POST.get("name")
        employee.role = request.POST.get("role")
        employee.department = request.POST.get("department")
        employee.designation = request.POST.get("designation")
        employee.salary = request.POST.get("salary")
        employee.phone = request.POST.get("phone")

        employee.save()
        messages.success(request, "Employee updated successfully!")
        return redirect("employee_list")

    return render(request, "edit_employee.html", {"employee": employee})


@login_required
@role_required(["Admin", "HR"])  # Only Admin and HR can delete employees
def delete_employee(request, employee_id):
    if request.method == 'POST':
        employee = get_object_or_404(Employee, id=employee_id)
        employee.delete()
        return JsonResponse({'message': 'Employee deleted successfully'})
    return JsonResponse({'message': 'Invalid request method'}, status=400)


def home(request):
    return render(request, "home.html")  # Make sure 'home.html' exists in templates


from django.shortcuts import render, get_object_or_404, redirect
from .models import Project, Task
from django.contrib.auth.decorators import login_required

@login_required
def project_details(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    # tasks = Task.objects.filter(project=project) 
    tasks = project.tasks.all()  # Fetch all tasks related to the project
    return render(request, 'project_details.html', {'project': project, 'tasks': tasks})


from django.shortcuts import render, get_object_or_404, redirect
from .models import Project
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

@login_required
def project_dashboard(request):
    projects = Project.objects.all().order_by('-created_at')  # Show recent projects first
    projects = Project.objects.prefetch_related('assigned_to').all()  # Optimized query
    return render(request, 'project_dashboard.html', {'projects': projects})

from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from myapp.models import Project  # Update this if your app name is different

@login_required
def mark_project_completed(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    
    # Update status and save
    project.status = "Completed"
    project.save(update_fields=['status'])  # Ensures only status updates

    return JsonResponse({
        'status': 'success',
        'message': 'Project marked as completed successfully.',
        'project_id': project_id
    })




@login_required
def mark_task_completed(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    task.status = "Completed"
    task.save(update_fields=['status'])  # Save only the status field

    return JsonResponse({
        'status': 'success',
        'message': 'Task marked as completed successfully.',
        'task_id': task_id
    })



@login_required
@role_required(['Admin', 'Manager'])
def add_project(request):
    employees = Employee.objects.all()

    if request.method == 'POST':
        name = request.POST['name']
        description = request.POST['description']
        end_date = request.POST['end_date']
        assigned_to_ids = request.POST.getlist('assigned_to')

        if not assigned_to_ids:
            return JsonResponse({'status': 'error', 'message': "Please select at least one employee."})

        project = Project.objects.create(
            name=name, description=description, end_date=end_date
        )

        employees_to_assign = Employee.objects.filter(id__in=assigned_to_ids)
        project.assigned_to.set(employees_to_assign)

        # ✅ Add a redirect URL for the success response
        return JsonResponse({
            'status': 'success',
            'message': "Project created successfully!",
            'redirect_url': reverse('project_dashboard')  # Use the correct URL name
        })

    return render(request, 'add_project.html', {'employees': employees})


@login_required
@role_required(['Admin', 'Manager'])
def edit_project(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    employees = Employee.objects.all()

    if request.method == 'POST':
        project.name = request.POST['name']
        project.description = request.POST['description']
        project.end_date = request.POST['end_date']

        selected_employee_ids = request.POST.getlist('assigned_to')
        project.assigned_to.set(selected_employee_ids)

        project.save()
        return redirect('project_dashboard')

    return render(request, 'edit_project.html', {'project': project, 'employees': employees})

@login_required
@role_required(['Admin'])  # Only Admin can delete
def delete_project(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    project.delete()

    return JsonResponse({'status': 'success', 'message': 'Project deleted successfully.'})




@login_required
@role_required(['Manager'])  # ✅ Ensures only Managers can access
def add_task(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    employees = Employee.objects.all()

    if request.method == 'POST':
        name = request.POST['name']
        description = request.POST['description']
        assignee_id = request.POST.get('assignee')
        priority = request.POST['priority']
        deadline = request.POST['deadline']

        if not assignee_id:
            messages.error(request, "Please select an employee.")
            return render(request, 'add_task.html', {'project': project, 'employees': employees})

        assignee = get_object_or_404(Employee, id=assignee_id)

        Task.objects.create(
            project=project, name=name, description=description,
            assignee=assignee, priority=priority, deadline=deadline
        )

        messages.success(request, "Task added successfully.")
        return redirect('project_details', project_id=project.id)

    return render(request, 'add_task.html', {'project': project, 'employees': employees})


@login_required
@role_required(['Manager'])
def edit_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)

    if request.method == 'POST':
        task.name = request.POST['name']
        task.description = request.POST['description']
        task.priority = request.POST['priority']
        task.status = request.POST['status']
        task.deadline = request.POST['deadline']
        task.save()
        messages.success(request, "Task updated successfully.")
        return redirect('project_details', project_id=task.project.id)

    return render(request, 'edit_task.html', {'task': task})


from django.shortcuts import render, redirect
from .models import LeaveRequest

def leave_request_view(request):
    if request.method == 'POST':
        leave_type = request.POST.get('leave_type')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        reason = request.POST.get('reason')
        
        LeaveRequest.objects.create(
            employee=request.user,
            leave_type=leave_type,
            start_date=start_date,
            end_date=end_date,
            reason=reason,
            status='Pending'  # Default status is pending
        )
        return redirect('leave_history')  # Redirect after submission
    
    return render(request, 'leave_request.html')

def leave_history_view(request):
    leaves = LeaveRequest.objects.filter(employee=request.user)
    return render(request, 'leave_history.html', {'leave_history': leaves})

def leave_approval_view(request):
    if request.user.is_superuser or request.user.groups.filter(name="HR").exists():
        pending_leaves = LeaveRequest.objects.filter(status="Pending")
        return render(request, 'leave_approval.html', {'pending_leaves': pending_leaves})
    else:
        return redirect('dashboard')
    
def approve_leave(request, leave_id):
    leave = get_object_or_404(LeaveRequest, id=leave_id)
    leave.status = "Approved"
    leave.save()
    return redirect('leave_approval')

def reject_leave(request, leave_id):
    leave = get_object_or_404(LeaveRequest, id=leave_id)
    leave.status = "Rejected"
    leave.save()
    return redirect('leave_approval')



from django.shortcuts import render
from .models import Task, Employee

def performance_dashboard(request):
    employees = Employee.objects.all()

    employee_performance = {}
    total_tasks = 0
    completed_tasks = 0
    pending_tasks = 0

    for employee in employees:
        total = Task.objects.filter(assignee=employee).count()
        completed = Task.objects.filter(assignee=employee, status="Completed").count()
        pending = total - completed  # Calculate pending tasks

        employee_performance[employee.name] = (completed, total)

        total_tasks += total
        completed_tasks += completed
        pending_tasks += pending

    context = {
        'total_tasks': total_tasks,
        'completed_tasks': completed_tasks,
        'pending_tasks': pending_tasks,
        'employee_performance': employee_performance
    }

    return render(request, 'performance_dashboard.html', context)


from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from myapp.models import Employee, Task  # Import required models

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from myapp.models import Employee, Task  

@login_required
def custom_report(request):
    department_filter = request.GET.get('department', 'All')
    role_filter = request.GET.get('role', 'All')

    employees = Employee.objects.all()  # Get all employees

    # Apply department filter
    if department_filter and department_filter != 'All':
        employees = employees.filter(department=department_filter)

    # Apply role filter
    if role_filter and role_filter != 'All':
        employees = employees.filter(role=role_filter)

    report_data = {}  # Initialize dictionary for report data

    for employee in employees:
        completed_tasks = Task.objects.filter(assignee=employee, status='Completed').count()
        report_data[employee.name] = completed_tasks  # Add to dictionary

    print("Filtered Employees:", employees)  # Debugging: Check employees
    print("Report Data:", report_data)  # Debugging: Check task count

    return render(request, 'custom_report.html', {'report_data': report_data})


from django.shortcuts import render
from .models import LeaveRequest
import datetime

def leave_trends(request):
    today = datetime.date.today()
    year = today.year
    months = [f"{month:02d}" for month in range(1, 13)]  # ['01', '02', ..., '12']
    
    leave_data = {
        month: LeaveRequest.objects.filter(start_date__month=month, start_date__year=year).count()
        for month in range(1, 13)
    }

    # Pass leave_data as a list of values (as a list of counts for months)
    leave_data_values = list(leave_data.values())

    return render(request, 'leave_trends.html', {
        'months': months,
        'leave_data_values': leave_data_values
    })


from django.shortcuts import render
from django.db.models import Q
from .models import Task, Employee
from django.utils.timezone import now 

def employee_productivity(request):
    productivity_data = {}

    for employee in Employee.objects.all():
        completed_tasks = Task.objects.filter(assignee=employee, status="Completed").count()

        
        on_time_tasks = sum(
            1 for task in Task.objects.filter(assignee=employee, status="Completed") 
            if task.deadline >= now().date()
        )

       
        pending_tasks = Task.objects.filter(
            assignee=employee, 
            status__in=["Pending", "In Progress"], 
            deadline__gte=now().date()  
        ).count()

        productivity_data[employee.name] = {
            "completed": completed_tasks,
            "on_time": on_time_tasks,
            "pending": pending_tasks
        }

    total_tasks = Task.objects.count()
    completed_tasks = Task.objects.filter(status="Completed").count()
    pending_tasks = Task.objects.filter(Q(status="Pending") | Q(status="In Progress"), deadline__gte=now().date()).count()

    return render(request, 'employee_productivity.html', {
        'productivity_data': productivity_data,
        'total_tasks': total_tasks,
        'completed_tasks': completed_tasks,
        'pending_tasks': pending_tasks
    })


from django.shortcuts import render
from .models import Employee, Task

def generate_report(request):
    # ✅ Hardcoded Department and Role Options
    departments = ["All", "HR", "IT", "Finance", "Marketing"]
    roles = ["All", "Admin", "Manager", "Employee"]

    # ✅ Get selected department & role from request
    department = request.GET.get("department", "All")
    role = request.GET.get("role", "All")

    print("🔍 Selected Department:", department)
    print("🔍 Selected Role:", role)

    # ✅ Filter employees correctly
    employees = Employee.objects.all()
    if department != "All":
        employees = employees.filter(department=department)
    if role != "All":
        employees = employees.filter(role=role)

    # ✅ Generate report data
    report_data = {
        employee.name: Task.objects.filter(assignee=employee, status="Completed").count()
        for employee in employees
    }

    return render(request, "custom_report.html", {
        "departments": departments,
        "roles": roles,
        "selected_department": department,  # ✅ Keeps selection
        "selected_role": role,  # ✅ Keeps selection
        "report_data": report_data,
    })

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import LeaveRequest, Task, Employee
from django.db.models import Q
from django.utils.timezone import now

# Utility functions for RBAC
def is_admin(user):
    return user.is_superuser

def is_hr(user):
    return user.groups.filter(name="HR").exists()

def is_manager(user):
    return user.groups.filter(name="Manager").exists()

def is_employee(user):
    return user.groups.filter(name="Employee").exists()

# LEAVE MANAGEMENT
@login_required
def leave_request_view(request):
    if request.method == 'POST' and is_employee(request.user):
        leave_type = request.POST.get('leave_type')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        reason = request.POST.get('reason')
        
        LeaveRequest.objects.create(
            employee=request.user,
            leave_type=leave_type,
            start_date=start_date,
            end_date=end_date,
            reason=reason,
            status='Pending'
        )
        return redirect('leave_history')
    
    return render(request, 'leave_request.html')

@login_required
def leave_history_view(request):
    leaves = LeaveRequest.objects.filter(employee=request.user)
    return render(request, 'leave_history.html', {'leave_history': leaves})

@login_required
@user_passes_test(lambda u: is_admin(u) or is_hr(u))
def leave_approval_view(request):
    pending_leaves = LeaveRequest.objects.filter(status="Pending")
    return render(request, 'leave_approval.html', {'pending_leaves': pending_leaves})

@login_required
@user_passes_test(lambda u: is_admin(u) or is_hr(u))
def approve_leave(request, leave_id):
    leave = get_object_or_404(LeaveRequest, id=leave_id)
    leave.status = "Approved"
    leave.save()
    return redirect('leave_approval')

@login_required
@user_passes_test(lambda u: is_admin(u) or is_hr(u))
def reject_leave(request, leave_id):
    leave = get_object_or_404(LeaveRequest, id=leave_id)
    leave.status = "Rejected"
    leave.save()
    return redirect('leave_approval')


@login_required
def communication_view(request):
    # Fetch notifications (for all users)
    notifications = Notification.objects.all().order_by('-created_at')

    # Fetch messages for the logged-in user
    messages_list = Message.objects.filter(recipient=request.user).order_by('-sent_at')

    # Fetch all announcements
    announcements = Announcement.objects.all().order_by('-created_at')

    # Handle sending a new notification (Only Admins can send)
    if request.method == 'POST' and 'create_notification' in request.POST:
        if not request.user.is_staff and not request.user.is_superuser:  # ❌ Block non-admins
            messages.error(request, "You are not authorized to send notifications.")
            return redirect('notifications_list')

        form = NotificationForm(request.POST)
        if form.is_valid():
            notification = form.save()
            messages.success(request, "Notification sent successfully.")
            return redirect('notifications_list')

    # Initialize forms
    message_form = MessageForm()
    announcement_form = AnnouncementForm()
    notification_form = NotificationForm() if request.user.is_staff or request.user.is_superuser else None  # ✅ Only admins get the form

    return render(request, 'messages_and_announcements.html', {
        'notifications': notifications,
        'messages': messages_list,
        'announcements': announcements,
        'message_form': message_form,
        'announcement_form': announcement_form,
        'notification_form': notification_form
    })








@login_required
def notifications_view(request):
    notifications = Notification.objects.all().order_by('-created_at')  # Fetch all notifications

    if request.method == 'POST' and 'create_notification' in request.POST:
        if request.user.is_staff or request.user.is_superuser:  # Admin check
            form = NotificationForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, "Notification sent to all users.")
                return redirect('notifications_list')
        else:
            messages.error(request, "You are not authorized to send notifications.")

    notification_form = NotificationForm() if request.user.is_staff or request.user.is_superuser else None

    return render(request, 'messages_and_announcements.html', {
        'notifications': notifications,
        'notification_form': notification_form
    })  # Remove 'messages' from context



@login_required
def inbox_view(request):
    """View for the user’s message inbox."""
    messages_list = Message.objects.filter(recipient=request.user).order_by('-sent_at')

    # ✅ Allow all users to send messages
    message_form = MessageForm()

    return render(request, 'messages_and_announcements.html', {
        'messages': messages_list,
        'message_form': message_form  # ✅ Always pass the form
    })








from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Announcement
from .forms import AnnouncementForm

@login_required
def announcements_view(request):
    """Allows admins to create announcements and users to view them."""
    announcements = Announcement.objects.all().order_by('-created_at')  # ✅ Fetch all

    if request.method == 'POST' and 'create_announcement' in request.POST:
        if not request.user.is_staff and not request.user.is_superuser:  # ✅ Block non-admins
            messages.error(request, "You are not authorized to create announcements.")
            return redirect('announcement_list')

        form = AnnouncementForm(request.POST)
        print("Form Data:", request.POST)  # ✅ Debugging: Print submitted data
        if form.is_valid():
            print("Form is valid.")  # ✅ Debugging: Confirm form validation
            announcement = form.save(commit=False)
            announcement.created_by = request.user  # ✅ Ensure admin is set
            announcement.save()
            messages.success(request, "Announcement created successfully.")
            return redirect('dashboard')  # ✅ Redirect to dashboard
        else:
            print("Form Errors:", form.errors)  # ✅ Debugging: Show form errors
            messages.error(request, "Invalid form submission. Please check your input.")

    # Show the form only if the user is an admin
    announcement_form = AnnouncementForm() if request.user.is_staff or request.user.is_superuser else None

    return render(request, 'messages_and_announcements.html', {
        'announcements': announcements,
        'announcement_form': announcement_form
    })

