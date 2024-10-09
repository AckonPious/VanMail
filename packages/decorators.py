import functools
from django.shortcuts import redirect
from django.contrib import messages
from functools import wraps

def admin_required(view_func, denied_url="dashboard"):
    @functools.wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.is_admin:
            return view_func(request, *args, **kwargs)
        messages.warning(request, "Page not found")
        return redirect(denied_url)  
    return wrapper

def registry_required(view_func, denied_url="dashboard"):
    @functools.wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if (request.user.is_authenticated and request.user.is_registry) or (request.user.is_authenticated and request.user.is_admin):
            return view_func(request, *args, **kwargs)
        messages.info(request, "Page not found")
        return redirect(denied_url)  
    return wrapper
