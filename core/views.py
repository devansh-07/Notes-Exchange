from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse, FileResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from .forms import RequestForm, UploadForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from core.models import Request, File
import os

# Create your views here.

@csrf_exempt
@require_http_methods(["GET"])
def download(request):
    fileid = request.GET['fileid']
    return FileResponse(open(os.path.join(os.getcwd(), 'core/Files/Page.pdf'), 'rb'))

def home(request):
    if request.user.is_authenticated:
        reqs = Request.objects.all().order_by('-date')
        all_files = File.objects.all()
        return render(request, "core/home.html", {"reqs": reqs, "files": all_files})
    else:
        return render(request, "core/general_home.html")

def about(request):
    return render(request, "core/about.html")

@login_required
def new_request(request):
    if request.method == "POST":
        form = RequestForm(request.POST)
        if form.is_valid():
            form.save(request, request.user)
            messages.success(request, f"New request created!")
            return redirect('home')
    else:
        form = RequestForm()
    return render(request, "core/requests.html", {"form": form})

@login_required
def new_upload(request):
    if request.method == "POST":
        form = UploadForm(request.POST, request.FILES)
        if form.is_valid():
            form.save(request, request.user)
            messages.success(request, f"New file uploaded!")
            return redirect('home')
    else:
        form = UploadForm()
    return render(request, "core/upload.html", {"form": form})


@login_required
def request_details(request, req_id):
    req = Request.objects.filter(id=req_id).first()
    if not req:
        messages.warning(request, f"Invalid request ID!")
        return redirect('home')
    return render(request, "core/request_detail.html", {"req": req})
