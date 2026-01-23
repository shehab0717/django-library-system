from django.urls import path
from . import views

app_name = "member"
urlpatterns = [
    path("", views.MmeberIndexView.as_view(), name="member_index"),
    path("add/", views.MmemberCreateView.as_view(), name="member_add"),
    path(
        "detail/<int:member_id>", views.MemberDetailView.as_view(), name="member_detail"
    ),
]
