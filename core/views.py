from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse, FileResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from .forms import RequestForm, UploadForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from core.models import Request, File
import os
from .filters import RequestFilter, FileFilter

# Create your views here.

@csrf_exempt
@require_http_methods(["GET"])
def download(request):
    fileid = request.GET['fileid']
    return FileResponse(open(os.path.join(os.getcwd(), 'core/Files/Page.pdf'), 'rb'))

def home(request):
    reqs = Request.objects.filter().order_by('-date')
    all_files = File.objects.all().order_by('-upload_date')
    return render(request, "core/home.html", {"reqs": reqs[:3], "files": all_files[:3]})

def all_requests(request):
    reqs = Request.objects.all()

    myfilter = RequestFilter(request.GET, queryset=reqs)
    new_reqs = myfilter.qs
    return render(request, "core/all_requests.html", {"reqs": new_reqs.order_by('-date'), 'myfilter': myfilter})

def all_files(request):
    all_files = File.objects.all()

    myfilter = FileFilter(request.GET, queryset=all_files)
    all_files = myfilter.qs
    return render(request, "core/all_files.html", {"files": all_files.order_by('-upload_date'), 'myfilter': myfilter})

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
    return render(request, "core/new_request.html", {"form": form})

@login_required
def close_request(request, req_id):
    req = Request.objects.filter(id=req_id).first()
    if not req:
        messages.warning(request, f"Invalid request ID!")
        return redirect('home')
    if req.user != request.user:
        messages.warning(request, f"Access denied.")
        return render(request, "core/request_detail.html", {"req": req})
    else:
        req.is_closed = True
        req.save()
    return redirect('request-details', req_id=req.id)

@login_required
def new_upload(request):
    if request.method == "POST":
        form = UploadForm(request.POST, request.FILES)
        if form.is_valid():
            form.save(request, request.user)
            messages.success(request, f"New file uploaded!")
            next = request.POST.get('next', 'all-uploads')
            return redirect(next)
    else:
        form = UploadForm(initial=request.GET)
    return render(request, "core/upload.html", {"form": form, "next": request.GET.get('next', 'all-uploads')})

def request_details(request, req_id):
    req = Request.objects.filter(id=req_id).first()
    if not req:
        messages.warning(request, f"Invalid request ID!")
        return redirect('home')
    return render(request, "core/request_detail.html", {"req": req})
