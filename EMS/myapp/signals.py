from django.contrib.auth.models import Group, Permission
from django.db.models.signals import post_migrate
from django.dispatch import receiver

@receiver(post_migrate)
def create_user_roles(sender, **kwargs):
    if sender.name == "myapp":
        admin_group, _ = Group.objects.get_or_create(name='Admin')
        hr_group, _ = Group.objects.get_or_create(name='HR')
        manager_group, _ = Group.objects.get_or_create(name='Manager')
        employee_group, _ = Group.objects.get_or_create(name='Employee')

        # Assign permissions (Modify as needed)
        admin_group.permissions.set(Permission.objects.all())  # Full access
        hr_group.permissions.set(Permission.objects.filter(codename__in=['view_employee', 'change_employee']))
        manager_group.permissions.set(Permission.objects.filter(codename__in=['view_project', 'change_project']))
        employee_group.permissions.set(Permission.objects.filter(codename__in=['view_own_profile']))
