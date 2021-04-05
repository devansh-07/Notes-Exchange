import os
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.

class Request(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=100)
    # college = models.CharField(max_length=100)
    branch = models.CharField(max_length=50)
    semester = models.IntegerField()
    date = models.DateTimeField(default=timezone.now)
    is_closed = models.BooleanField(default=False)

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

class File(models.Model):
    doc = models.FileField(upload_to='Files/', default="0")
    # college = models.CharField(max_length=100)
    description = models.CharField(max_length=100)
    branch = models.CharField(max_length=50)
    semester = models.IntegerField()
    upload_date = models.DateTimeField(default=timezone.now)

    # Foreign Keys
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    request = models.ForeignKey(Request, on_delete=models.CASCADE, null=True)

    @property
    def filename(self):
        return os.path.basename(self.doc.name)

    def __str__(self):
        return self.filename
