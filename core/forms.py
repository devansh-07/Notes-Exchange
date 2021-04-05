from django import forms
from . import choices
from .models import Request, File
from django.db.models.fields import BLANK_CHOICE_DASH
from django.core.validators import FileExtensionValidator

class RequestForm(forms.Form):
    title = forms.CharField(label='Title', max_length=100)
    description = forms.CharField(label='Description', max_length=500)
    # college = forms.ChoiceField(label='College', widget=forms.Select, choices=choices.colleges)
    branch = forms.ChoiceField(label='Branch', widget=forms.Select, choices=BLANK_CHOICE_DASH + choices.branches)
    semester = forms.ChoiceField(label='Semester', widget=forms.Select, choices=BLANK_CHOICE_DASH + choices.semesters)

    def save(self, request, user):
        data = self.cleaned_data
        new_req = Request.objects.create(title=data['title'], description=data['description'], branch=data['branch'], semester=data['semester'], user_id=user.id)
        new_req.save()

class UploadForm(forms.Form):
    doc = forms.FileField(validators=[FileExtensionValidator(['pdf'])], label='Upload File (PDF format only)')
    description = forms.CharField(label='Description', max_length=500)
    branch = forms.ChoiceField(label='Branch', widget=forms.Select, choices=BLANK_CHOICE_DASH + choices.branches)
    semester = forms.ChoiceField(label='Semester', widget=forms.Select, choices=BLANK_CHOICE_DASH + choices.semesters)

    def save(self, request, user):
        data = self.cleaned_data
        new_file = File.objects.create(doc=data['doc'], description=data['description'], branch=data['branch'], semester=data['semester'], user_id=user.id)
        new_file.save()
