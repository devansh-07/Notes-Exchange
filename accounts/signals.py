from django.db.models.signals import post_save
from django.contrib.auth.signals import user_logged_out
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.contrib import messages
from .models import Profile

def show_message(sender, user, request, **kwargs):
    # messages.info(request, 'You have been logged out.')
    pass

user_logged_out.connect(show_message)
