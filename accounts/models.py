from django.db import models
from django.utils import timezone

# NEEDED FOR AUTHENTICATION
from django.contrib.auth.models import User
# Add Unique constraint for User model
User._meta.get_field('email')._unique = True

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # college = models.CharField(max_length=100)
    branch = models.CharField(max_length=50)
    semester = models.IntegerField()
    # rollno = models.CharField(max_length=15)

    def __str__(self):
        return self.user.username
