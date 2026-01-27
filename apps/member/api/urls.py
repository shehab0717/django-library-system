from django.urls import path
from .views import MemberListView


urlpatterns = [
    path("members/", MemberListView.as_view(), name="members"),
]
