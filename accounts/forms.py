from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from core import choices

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField()
    # college = forms.CharField(max_length=50)
    branch = forms.ChoiceField(label='Branch', widget=forms.Select, choices=choices.branches)
    semester = forms.ChoiceField(label='Semester', widget=forms.Select, choices=choices.semesters)
    # rollno = forms.CharField(max_length=15)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'email', 'branch', 'semester', 'password1', 'password2')
        labels = {
            "first_name": "Name",
            'branch': "Branch/Stream"
        }
