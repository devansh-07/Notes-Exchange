from django.urls import path
from . import views

urlpatterns = [
    path('users/', views.users, name='users'),
    path('files/', views.files, name='files'),
    path('requests/', views.requests, name='requests'),
]
