from django.shortcuts import render
from django.http import JsonResponse, HttpResponse, FileResponse
from django.views.decorators.csrf import csrf_exempt

import os
from accounts.models import Profile
from core.models import File, Request

# Create your views here.
def home(request):
    return render(request, 'index.html')

@csrf_exempt
def users(request):
    if request.method == "POST":

        print(request.POST)
        data = request.POST
        uname = data['username']

        if Profile.objects.filter(username=uname).first() is not None:
            return JsonResponse({"Error": "Username already Exists"}, status=409)

        if Profile.objects.filter(email=data['email']).first() is not None:
            return JsonResponse({"Error": "Email already registered"}, status=409)

        if Profile.objects.filter(rollno=data['rollno'], college=data['college']).first() is not None:
            return JsonResponse({"Error": "User with this roll no. already registered"}, status=409)

        user = Profile.objects.create_user(username=data["username"], name=data["name"], email=data["email"], college=data["college"], branch=data["branch"], semester=data["semester"], rollno=data["rollno"], password=data["password"])
        user.save()

        return HttpResponse("Data submitted.", status=201)

    elif request.method == "GET":
        try:
            uname = request.GET['username']
        except:
            return JsonResponse({"username": "This field is required."}, status=400)

        user = Profile.objects.filter(username=uname).first()

        if not user:
            return JsonResponse({"message": "This username doesn't exist in the database."}, status=404)

        udata = {
            "username": user.username,
            "email": user.email,
            "name": user.name,
            "college": user.college,
            "branch": user.branch,
            "semester": user.semester,
            "rollno": user.rollno,
            "password": user.password,
            "files": [f.id for f in File.objects.filter(user=user.username)],
            "requests": [r.id for r in Request.objects.filter(user=user.username)]
        }

        return JsonResponse(udata, status=200)

@csrf_exempt
def files(request):
    data = {
        'fileid': 1,
        'filename': 'B Tech 5th sem CSE Syllabus.pdf'
    }

    if request.method == "POST":
        return HttpResponse("Data submitted.", status=201)
    elif request.method == "GET":
        try:
            f_id = request.GET['fileid']
        except:
            return JsonResponse({"fileid": "This field is required."}, status=400)

        file = File.objects.filter(id=f_id).first()

        if not file:
            return JsonResponse({"message": "No such file exist in the database."}, status=404)

        file_data = {
            "id": file.id,
            "filename": file.filename,
            "college": file.college,
            "branch": file.branch,
            "semester": file.semester,
            "upload_date": file.upload_date,
            "user": file.user_id,
            "requestid": file.request_id
        }

        return JsonResponse(file_data, status=200)

@csrf_exempt
def requests(request):
    data = {
        'requestid': 1,
        'title': "Upload 2020 CSE 5th sem CGM Exam paper",
        "description": "I need 2018 CSE 5th sem CGM Exam paper urgently.",
        "user": "devansh07"
    }

    if request.method == "POST":
        return HttpResponse("Data submitted.", status=201)
    elif request.method == "GET":
        try:
            req_id = request.GET['requestid']
        except:
            return JsonResponse({"requestid": "This field is required."}, status=400)

        req = Request.objects.filter(id=req_id).first()

        if not req:
            return JsonResponse({"message": "No such request exist in the database."}, status=404)

        request_data = {
            "id": req.id,
            "title": req.title,
            "description": req.description,
            "college": req.college,
            "branch": req.branch,
            "semester": req.semester,
            "date": req.date,
            "is_closed": req.is_closed,
            "user": req.user_id,
        }

        return JsonResponse(request_data, status=200)
