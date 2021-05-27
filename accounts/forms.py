from django import forms
from django.contrib.auth.models import User
from allauth.account.forms import SignupForm
from core import choices
from .models import Profile
from django.db.models.fields import BLANK_CHOICE_DASH
from django.core.validators import validate_image_file_extension

class CustomSignupForm(SignupForm):
    def __init__(self, *args, **kwargs):
        kwargs['email_required'] = True
        super(CustomSignupForm, self).__init__(*args, **kwargs)

class UserRegistrationForm(SignupForm):
    first_name = forms.CharField(label='Name', max_length=100, required=True)
    branch = forms.ChoiceField(label='Branch/Stream', widget=forms.Select, choices=choices.branches)
    semester = forms.ChoiceField(label='Semester', widget=forms.Select, choices=choices.semesters)
    # college = forms.CharField(max_length=50)
    # rollno = forms.CharField(max_length=15)

    field_order = ['username', 'first_name', 'email', 'branch', 'semester', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        kwargs['email_required'] = True
        super(UserRegistrationForm, self).__init__(*args, **kwargs)
        self.fields['email'].required = True

    def save(self, request, commit=True):
        if self.is_valid():
            user = super(UserRegistrationForm, self).save(request)

            username = self.cleaned_data.get('username')
            branch = self.cleaned_data.get('branch')
            semester = self.cleaned_data.get('semester')
            # rollno = self.cleaned_data.get('rollno')
            # college = self.cleaned_data.get('college')

            profile = Profile.objects.create(user=user, branch=branch, semester=semester)
            profile.save()

            return user
        else:
            raise ValueError('Invalid form data')


class ProfileUpdateForm(forms.ModelForm):
    first_name = forms.CharField(label='Name', max_length=100, required=True)

    def save(self, request, user):
        data = self.cleaned_data

        user = User.objects.get(id=user.id)
        user.first_name = data['first_name']
        user.save()

        if Profile.objects.filter(user_id=user.id).first():
            profile = Profile.objects.filter(user_id=user.id).first()
            profile.about = data['about']
            profile.website = data['website']
            profile.branch = data['branch']
            profile.semester = data['semester']
            profile.college = data['college']
            profile.save()
        else:
            profile = Profile.objects.create(user_id=user.id, about=data['about'], website=data['website'], branch=data['branch'], semester=data['semester'], college=data['college'])
            profile.save()

    class Meta:
        model = Profile
        fields = ['first_name', 'about', 'website', 'college', 'branch', 'semester']
        labels = {
            'about': "About me"
        }
        widgets = {
          'about': forms.Textarea(attrs={'rows': 3}),
        }
