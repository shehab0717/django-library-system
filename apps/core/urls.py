from django.contrib.auth.views import LoginView
from django.views.generic import TemplateView
from django.urls import path
from . import views


urlpatterns = [
    path("user/login/", LoginView.as_view(next_page="/user/profile/"), name="login"),
    path("user/profile/", views.UserProfileView.as_view(), name="user_profile"),
    path("", TemplateView.as_view(template_name="home.html"), name="home"),
]
