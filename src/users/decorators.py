# src/users/decorators.py
from functools import wraps

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect


def role_required(allowed_roles):
    """
    Restrict a function view to specific role(s).
    Example: @role_required(["teacher"]) or @role_required(["admin", "teacher"])
    """

    def decorator(view_func):
        @wraps(view_func)
        @login_required
        def wrapper(request, *args, **kwargs):
            role = getattr(request.user, "role", None)
            if role not in allowed_roles:
                messages.error(request, "You do not have permission to view this page.")
                # Send them to their own landing page
                return redirect("users:student_home")
            return view_func(request, *args, **kwargs)

        return wrapper

    return decorator
