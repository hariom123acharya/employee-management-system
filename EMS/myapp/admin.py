from django.contrib import admin
from .models import Employee
from django.contrib import admin
from myapp.models import Employee

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ("name", "user")
