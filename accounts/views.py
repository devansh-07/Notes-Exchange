from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import User, Profile
from core.models import File, Request
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from PIL import Image
from .forms import UserRegistrationForm, ProfileUpdateForm
from allauth.account.decorators import verified_email_required
import mimetypes
import os
import secrets

@login_required
@verified_email_required
def profile(request, username):
    user = User.objects.filter(username=username).first()
    if user:
        reqs = Request.objects.filter(user=user).order_by('-date')
        return render(request, "accounts/profile.html", {"usr": user, "reqs": reqs, "title": user.username})

    messages.warning(request, f"Username {username} doesn't exist!")
    return redirect('home')

@login_required
@verified_email_required
def update_profile(request):
    user = request.user
    if request.method == "GET":
        profile = Profile.objects.filter(user=user).first()
        if profile:
            data = profile.__dict__
            data['first_name'] = user.first_name
        else:
            data = None
        form = ProfileUpdateForm(data)
        next = request.GET.get('next')

        return render(request, "accounts/update_profile.html", {"form": form, "usr": user, "next": next, "title": "Edit profile - "+user.username})
    elif request.method == "POST":
        data = request.POST
        next = data.get("next", None)
        form = ProfileUpdateForm(data)
        if form.is_valid():
            form.save(request, user)
            if next:
                return redirect(next)

            return redirect('profile', username=user.username)
        else:
            pass
    return render(request, "accounts/update_profile.html", {"form": ProfileUpdateForm(), "usr": user, "title": "Edit profile - "+user.username})

@login_required
@verified_email_required
def update_profile_pic(request):
    user = request.user
    if request.method == "GET":
        next = request.GET.get('next')
        return redirect('update-profile')
    elif request.method == "POST":
        if not Profile.objects.filter(user_id=user.id).exists():
            messages.warning(request, "You have to complete your profile before you can change your profile picture.")
            return redirect('update-profile')

        data = request.FILES
        avatar = data.get("avatar")

        if not avatar:
            messages.warning(request, "No Image uploaded.")
            return redirect('update-profile')

        if mimetypes.guess_type(str(avatar.name))[0] not in ["image/jpeg", "image/png"]:
            messages.warning(request, "Invalid File Format.")
            return redirect('update-profile')

        try:
            img = Image.open(avatar)
        except:
            messages.warning(request, "Corrupted Image File.")
            return redirect('update-profile')

        random_hex = secrets.token_hex(8)
        _, fl_ext = os.path.splitext(avatar.name)

        avatar.name = random_hex + fl_ext
        profile = user.profile
        profile.avatar = avatar
        profile.save()

        img = Image.open(profile.avatar.path)

        if img.width != img.height:
            width, height = img.size
            new_dim = min(width, height)

            left = (width - new_dim)/2
            top = (height - new_dim)/2
            right = (width + new_dim)/2
            bottom = (height + new_dim)/2

            img = img.crop((left, top, right, bottom))

        output_size = (360, 360)
        img.thumbnail(output_size)
        img.save(profile.avatar.path)

        return redirect('update-profile')

    return redirect('update-profile')















    user = request.user
    if request.method == "POST":
        if not Profile.objects.filter(user_id=user.id).exists():
            messages.warning(request, "You have to complete your profile before you can change your profile picture.")
            return render(request, "accounts/update_profile.html", {"form": ProfileUpdateForm(), "usr": user})
        else:
            data = request.FILES
            avatar = data['avatar']

            print(avatar)
            if avatar:
                profile = user.profile
                profile.avatar = avatar
                profile.save()

                try:
                    img = Image.open(profile.avatar.path)

                    if img.width != img.height:
                        width, height = img.size

                        new_dim = min(width, height)

                        left = (width - new_dim)/2
                        top = (height - new_dim)/2
                        right = (width + new_dim)/2
                        bottom = (height + new_dim)/2

                        img = img.crop((left, top, right, bottom))

                    if img.width > 360 or img.height > 360:
                        output_size = (360, 360)
                        img.thumbnail(output_size)
                        img.save(profile.avatar.path)

                    return redirect('update-profile')
                except:
                    messages.warning(request, "Error occured.")
                    return render(request, "accounts/update_profile.html", {"form": ProfileUpdateForm(), "usr": user})

        return redirect('update-profile')
    return render(request, "accounts/update_profile.html", {"form": ProfileUpdateForm(), "usr": user, "title": "Edit profile - "+user.username})
