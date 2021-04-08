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

    # Choices were not getting updated as the module is loaded at startup only
    # https://www.codementor.io/tips/7714213398/django-form-choices-loaded-from-database-are-not-updated#:~:text=That's%20because%20module%20is%20loaded,__%20on%20the%20form%20class.

    def __init__(self, *args, **kwargs):
        super(UploadForm, self).__init__(*args, **kwargs)
        try:
            request_choices = [(req.id, req.title) for req in Request.objects.all()]
        except:
            request_choices = []
        self.fields['req'] = forms.ChoiceField(label='Request (Optional)', widget=forms.Select, choices=BLANK_CHOICE_DASH + request_choices, required=False)

    doc = forms.FileField(validators=[FileExtensionValidator(['pdf'])], label='Upload File (PDF format only)')
    description = forms.CharField(label='Description', max_length=500)
    branch = forms.ChoiceField(label='Branch', widget=forms.Select, choices=BLANK_CHOICE_DASH + choices.branches)
    semester = forms.ChoiceField(label='Semester', widget=forms.Select, choices=BLANK_CHOICE_DASH + choices.semesters)
    req = forms.ChoiceField(label='Request (Optional)', widget=forms.Select, choices=BLANK_CHOICE_DASH, required=False)

    def save(self, request, user):
        data = self.cleaned_data
        reqt = Request.objects.filter(id=data['req']).first() if data['req'] else None
        new_file = File.objects.create(doc=data['doc'], description=data['description'], branch=data['branch'], semester=data['semester'], user_id=user.id, request=reqt)
        new_file.save()
