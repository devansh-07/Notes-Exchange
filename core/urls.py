from django.urls import path
from . import views

from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('', views.home, name='home'),
    path('home/', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('requests/new', views.new_request, name='new-request'),
    path('requests/all', views.all_requests, name='all-requests'),
    path('uploads/new', views.new_upload, name='new-upload'),
    path('uploads/all', views.all_files, name='all-uploads'),
    path('request/<int:req_id>', views.request_details, name='request-details'),
    path('request/<int:req_id>/<int:file_id>/close', views.close_request, name='close-request'),
    path('download/', views.download, name='download'),
    path('media/profile_pics/<str:filename>', views.profile_pic_server, name='media-server'),
    path('cast-vote/', views.cast_vote, name='cast-vote'),

    # API URLs
    path('test/', views.TestView.as_view(), name='test'),
    path('test-req/', views.RequestListCreateView.as_view(), name='test-req'),
    # path('test-file/', views.FileListCreateView.as_view(), name='test-file'),
    path('api/token/', obtain_auth_token, name="get-token")
]
