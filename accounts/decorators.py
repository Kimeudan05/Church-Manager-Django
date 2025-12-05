from django.shortcuts import redirect
from django.contrib import messages
from functools import wraps


def role_required(*allowed_roles):
    """
    Decorator: restricts access to users whose profile.role is inside allowed_roles
    """

    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            # if user is not logged in
            if not request.user.is_authenticated:
                messages.error(request, "You must be logged in to view this page.")
                return redirect("accounts:login")
            user_role = request.user.profile.role

            # if user is logged in but not allowed
            if user_role not in allowed_roles:
                messages.error(
                    request, "You do not have permission to access this page."
                )
                return redirect("dashboard:index")

            return view_func(request, *args, **kwargs)

        return wrapper

    return decorator
