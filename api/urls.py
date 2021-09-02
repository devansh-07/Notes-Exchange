from django.urls import path
from . import views
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('profile/<str:username>', views.ProfileDetailView.as_view(), name='user-profile'),

    path('requests/', views.ListRequestView.as_view(), name='get-requests'),
    path('requests/<int:id>/', views.GetRequestDetailView.as_view(), name='get-request-detail'),
    path('requests/<int:id>/new_response/', views.NewResponseView.as_view(), name='new-response'),

    path('files/', views.ListFileView.as_view(), name='get-files'),
    path('files/<int:id>', views.GetFileView.as_view(), name='get-single-file'),

    path('get_token/', obtain_auth_token, name="get-token"),
]
