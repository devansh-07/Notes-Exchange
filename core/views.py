from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse, FileResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from .forms import RequestForm, UploadForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from core.models import Request, File
import os
from .filters import RequestFilter, FileFilter
from accounts.decorators import profile_required
from allauth.account.decorators import verified_email_required
from accounts.forms import CustomSignupForm
from allauth.account.forms import LoginForm

# Create your views here.

global file_upload_path
file_upload_path = "files/"

def mtest(request):
    f = File.objects.filter(request=2)
    print(f.first(), f.all())
    return render(request, "index.html")

@require_http_methods(["GET"])
def download(request, filename):
    file_obj = File.objects.filter(doc=file_upload_path+filename).first()

    if not file_obj:
        messages.warning(request, "Invalid File name.")
        return redirect('home')

    return FileResponse(open(os.path.join(os.getcwd(), 'Media/files/', file_obj.filename), 'rb'))

def profile_pic_server(request, filename):
    return FileResponse(open(os.path.join(os.getcwd(), 'Media/profile_pics/', filename), 'rb'))

def home(request):
    if request.method == "GET":
        signupform = CustomSignupForm()
        loginform = LoginForm()

        reqs = Request.objects.filter().order_by('-date')
        all_files = File.objects.all().order_by('-upload_date')

        return render(request, "core/home.html", {"user": request.user, "reqs": reqs, "files": all_files, "title": "Home", 'loginform': loginform,'signupform': signupform})

    return render(request, "core/home.html")

# API created
def all_requests(request):
    signupform = CustomSignupForm()
    loginform = LoginForm()

    reqs = Request.objects.all()

    myfilter = RequestFilter(request.GET, queryset=reqs)
    new_reqs = myfilter.qs
    return render(request, "core/all_requests.html", {"reqs": new_reqs.order_by('-date'), 'myfilter': myfilter, "title": "All Requests", 'loginform': loginform,'signupform': signupform})

# API created
def all_files(request):
    signupform = CustomSignupForm()
    loginform = LoginForm()

    all_files = File.objects.all()

    myfilter = FileFilter(request.GET, queryset=all_files)
    all_files = myfilter.qs
    return render(request, "core/all_files.html", {"files": all_files.order_by('-upload_date'), 'myfilter': myfilter, "title": "All Files", 'loginform': loginform,'signupform': signupform})

def about(request):
    signupform = CustomSignupForm()
    loginform = LoginForm()
    return render(request, "core/about.html", {"title": "About Us", 'loginform': loginform,'signupform': signupform})

# API created
@login_required
@verified_email_required
@profile_required(redirect_url="update-profile")
def new_request(request):
    if request.method == "POST":
        form = RequestForm(request.POST)
        if form.is_valid():
            req = form.save(request, request.user)
            messages.success(request, f"New request created!")
            return redirect('request-details', req_id=req.id)
    else:
        form = RequestForm()
    return render(request, "core/new_request.html", {"form": form, "title": "Create new request"})

@login_required
def close_request(request, req_id, file_id):
    req = Request.objects.filter(id=req_id).first()
    if not req:
        messages.warning(request, f"Invalid request ID!")
        return redirect('home')

    file = File.objects.filter(id=file_id).first()
    if not file:
        messages.warning(request, f"Invalid File ID!")
        return redirect('home')

    if req.user != request.user:
        messages.warning(request, f"Access denied.")
        return redirect('request-details', req_id=req.id)
    else:
        req.closing_response = file
        req.save()

    return redirect('request-details', req_id=req.id)

@login_required
@verified_email_required
@profile_required(redirect_url="update-profile")
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
    return render(request, "core/upload.html", {"form": form, "next": request.GET.get('next', 'all-uploads'), "title": "Upload a Response"})

def request_details(request, req_id):
    signupform = CustomSignupForm()
    loginform = LoginForm()

    req = Request.objects.filter(id=req_id).first()
    if not req:
        messages.warning(request, f"Invalid request ID!")
        return redirect('home')
    return render(request, "core/request_detail.html", {"req": req, "title": req.title, 'loginform': loginform,'signupform': signupform})

@csrf_exempt
@login_required
@verified_email_required
@profile_required(redirect_url="update-profile")
def cast_vote(request):
    flag = request.POST.get("flag")
    vote = request.POST.get("vote")
    id = request.POST.get("object_id")
    user = request.user

    if flag == None or vote == None or id == None or flag not in ['0', '1'] or vote not in ['1', '-1']:
        # Invalid Input Code / Bad request
        return HttpResponse(status=400)

    try:
        id = int(id)

        if flag == '0':
            # Casting Vote for request
            object = Request.objects.get(id=id)
        else:
            # Casting Vote for Upload
            object = File.objects.get(id=id)

        if vote == '1':
            # Upvote

            if user in object.upvotes.all():
                object.upvotes.remove(user)
            else:
                object.upvotes.add(user)
                object.downvotes.remove(user)

            return HttpResponse(status=201)
        else:
            # Downvote

            if user in object.downvotes.all():
                object.downvotes.remove(user)
            else:
                object.downvotes.add(user)
                object.upvotes.remove(user)

            return HttpResponse(status=201)
    except:
        # Invalid Input Code / Bad Request
        return HttpResponse(status=400)

    return HttpResponse(status=400)
