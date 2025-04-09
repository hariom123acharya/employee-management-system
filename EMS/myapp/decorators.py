from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect

def role_required(allowed_roles):
    def decorator(view_func):
        def wrapper(request, *args, **kwargs):
            if request.user.is_superuser:  # Allow superusers full access
                return view_func(request, *args, **kwargs)
            
            user_groups = request.user.groups.values_list('name', flat=True)  # Get user roles

            if any(role in user_groups for role in allowed_roles):
                return view_func(request, *args, **kwargs)

            return redirect('no_permission')  # Redirect to an error page
        return wrapper
    return decorator
