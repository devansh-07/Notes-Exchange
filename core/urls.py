from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('home/', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('requests/new', views.new_request, name='new-request'),
    path('requests/all', views.all_requests, name='all-requests'),
    path('uploads/new', views.new_upload, name='new-upload'),
    path('uploads/all', views.all_files, name='all-uploads'),
    path('request/<int:req_id>', views.request_details, name='request-details'),
    path('request/<int:req_id>/close', views.close_request, name='close-request'),
    path('download/', views.download, name='download')
]
