from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('profile/<str:username>', views.profile, name='profile'),
    path('update_profile', views.update_profile, name='update-profile'),
    path('update_profile_pic', views.update_profile_pic, name='update-profile-pic'),
    # path('login', auth_views.LoginView.as_view(redirect_authenticated_user=True, template_name="accounts/login.html"), name='login'),
    # path('logout', auth_views.LogoutView.as_view(template_name="core/general_home.html"), name='logout'),
]
