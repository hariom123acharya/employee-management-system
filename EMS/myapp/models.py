from django.db import models
from django.conf import settings  # Use the correct reference to the user model

from django.utils import timezone
from decimal import Decimal
from django.db import models
from django.conf import settings  # Import the correct user model





# class Employee(models.Model):
    
#     user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True, default=None)
#     name = models.CharField(max_length=100, blank=True, null=True, default="") 
#     email = models.EmailField(unique=True, default="")
#     phone = models.CharField(max_length=15, blank=True, null=True, default="")
#     designation = models.CharField(max_length=100, blank=True, null=True, default="")
#     salary = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    
    
#     department_choices = [
#         ("HR", "HR"),
#         ("Engineering", "Engineering"),
#         ("Marketing", "Marketing"),
#         ("Sales", "Sales"),
#     ]
#     department = models.CharField(max_length=50, choices=department_choices, default="HR")

#     role_choices = [
#         ("Admin", "Admin"),
#         ("HR", "HR"),
#         ("Manager", "Manager"),
#         ("Employee", "Employee"),
#     ]
#     role = models.CharField(max_length=50, choices=role_choices, default="Employee")
    
#     date_joined = models.DateField(auto_now_add=True)  # Automatically set when created

#     def __str__(self):
#         return f"{self.name} - {self.role} - {self.department}"  # Better display
from django.db import models
from django.conf import settings  # Import Django's user model
from decimal import Decimal  # Ensure DecimalField works correctly

class Employee(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=100, blank=True, null=True, default="") 
    email = models.EmailField(unique=True)  # Required field, unique
    phone = models.CharField(max_length=15, blank=True, null=True)
    designation = models.CharField(max_length=100, blank=True, null=True)
    salary = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))  # Ensure decimal is imported

    # Department Choices
    DEPARTMENT_CHOICES = [
        ("hr", "HR"),
        ("engineering", "Engineering"),
        ("marketing", "Marketing"),
        ("sales", "Sales"),
    ]
    department = models.CharField(max_length=50, choices=DEPARTMENT_CHOICES, default="hr")

    # Role Choices
    ROLE_CHOICES = [
        ("admin", "Admin"),
        ("hr", "HR"),
        ("manager", "Manager"),
        ("employee", "Employee"),
    ]
    role = models.CharField(max_length=50, choices=ROLE_CHOICES, default="employee")  # Default should be lowercase

    date_joined = models.DateField(auto_now_add=True)  # Automatically set when created

    def __str__(self):
        return f"{self.name} - {self.role.capitalize()} - {self.department.capitalize()}"



from django.db import models
from django.utils import timezone

class Project(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    status = models.CharField(
        max_length=20, 
        choices=[('Active', 'Active'), ('Completed', 'Completed'), ('On Hold', 'On Hold')], 
        default='Active'
    )
    start_date = models.DateField(default=timezone.now)
    end_date = models.DateField(null=True, blank=True)
    assigned_to = models.ManyToManyField('Employee', related_name='projects', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)  # New field to track creation time

    def __str__(self):
        return self.name

from django.contrib.auth.models import AbstractUser


from django.db import models

class Task(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='tasks')
    name = models.CharField(max_length=200)
    description = models.TextField()
    assignee = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True, blank=True)
    priority = models.CharField(max_length=20, choices=[('Low', 'Low'), ('Medium', 'Medium'), ('High', 'High')], default='Medium')
    status = models.CharField(max_length=20, choices=[('Not Started', 'Not Started'), ('In Progress', 'In Progress'), ('Completed', 'Completed')], default='Not Started')
    deadline = models.DateField()
    comments = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


from django.db import models
from django.contrib.auth.models import User

class LeaveRequest(models.Model):
    LEAVE_CHOICES = [
        ('Vacation', 'Vacation'),
        ('Sick', 'Sick'),
        ('Personal', 'Personal'),
        ('Other', 'Other')
    ]
    
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected')
    ]
    
    employee = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    leave_type = models.CharField(max_length=20, choices=LEAVE_CHOICES)
    start_date = models.DateField()
    end_date = models.DateField()
    reason = models.TextField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Pending')
    
    def __str__(self):
        return f"{self.employee.username} - {self.leave_type} - {self.status}"


from django.conf import settings
from django.db import models

class Notification(models.Model):
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    read_by = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='read_notifications', blank=True)

    def __str__(self):
        return f"Notification - {self.message[:50]}"


class Message(models.Model):
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='sent_messages')
    recipient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='received_messages')
    subject = models.CharField(max_length=200)
    body = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"Message from {self.sender.username} to {self.recipient.username}"


class Announcement(models.Model):
    title = models.CharField(max_length=255)
    body = models.TextField()
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Announcement: {self.title}"


from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):  
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('hr', 'HR'),
        ('manager', 'Manager'),
        ('employee', 'Employee'),
    ]

    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='employee')

    def __str__(self):
        return f"{self.username} ({self.role})"


