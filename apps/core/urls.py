from django.contrib.auth.views import LoginView
from django.urls import path
from . import views


urlpatterns = [
    path("user/login/", LoginView.as_view(next_page="/user/profile/"), name="login"),
    path("user/profile/", views.UserProfileView.as_view(), name="user_profile"),
]
