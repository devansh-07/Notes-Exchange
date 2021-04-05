from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('requests/new', views.new_request, name='new-request'),
    path('uploads/new', views.new_upload, name='new-upload'),
    path('request/<int:req_id>', views.request_details, name='request-details'),
    path('download/', views.download, name='download')
]
