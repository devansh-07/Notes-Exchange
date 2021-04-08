import django_filters
from .models import *

class RequestFilter(django_filters.FilterSet):
    class Meta:
        model = Request
        fields = ["branch", "semester"]

class FileFilter(django_filters.FilterSet):
    class Meta:
        model = File
        fields = ["branch", "semester"]
