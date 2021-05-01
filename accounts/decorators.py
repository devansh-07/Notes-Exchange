from django.contrib import messages
from django.shortcuts import render, redirect
from functools import wraps

def profile_required(redirect_url=None, next=None):
    def decorator(view_func):
        @wraps(view_func)
        def inner(request, *args, **kwargs):
            if not hasattr(request.user, "profile"):
                messages.warning(request, "You have to complete your profile to access this page")
                return redirect(redirect_url)

            return view_func(request, *args, **kwargs)

        return inner
    return decorator
