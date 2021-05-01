from django.db import models
from django import forms
from django.db.models.fields import BLANK_CHOICE_DASH
from core import choices
from django.utils import timezone

# NEEDED FOR AUTHENTICATION
from django.contrib.auth.models import User

# Add Unique constraint for User model
User._meta.get_field('email')._unique = True

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    avatar = models.ImageField(default='profile_pics/default-avatar.jpg', upload_to="profile_pics")
    about = models.TextField(blank=True)
    website = models.URLField(blank=True)
    branch = models.CharField(max_length=50, choices=BLANK_CHOICE_DASH+choices.branches)
    semester = models.IntegerField( choices=BLANK_CHOICE_DASH+choices.semesters)
    college = models.CharField(max_length=100)
    # rollno = models.CharField(max_length=15)

    def __str__(self):
        return self.user.username
