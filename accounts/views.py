from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import User, Profile
from core.models import File, Request
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .forms import UserRegistrationForm

def register(request):
    # To prevent user from registering if he is already logged in
    if request.user.is_authenticated:
        messages.info(request, f"You are already registered and logged In!")
        return redirect('home')

    if request.method == "GET":
        form = UserRegistrationForm()
    else:
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')

            # college = form.cleaned_data.get('college')
            branch = form.cleaned_data.get('branch')
            semester = form.cleaned_data.get('semester')
            rollno = form.cleaned_data.get('rollno')

            profile = Profile.objects.create(user=User.objects.filter(username=username).first(), branch=branch, semester=semester)
            profile.save()

            messages.success(request, f"Account created for {username}!")
            return redirect('login')
    return render(request, "accounts/register.html", {'form': form})

@login_required
def profile(request, username):
    user = User.objects.filter(username=username).first()
    if user:
        reqs = Request.objects.filter(user=user).order_by('-date')
        return render(request, "accounts/profile.html", {"usr": user, "reqs": reqs})

    messages.warning(request, f"Username {username} doesn't exist!")
    return redirect('home')
