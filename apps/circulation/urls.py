from django.urls import path
from . import views
from django.views.generic import TemplateView

app_name = "circulation"
urlpatterns = [
    path("", views.CirculationIndexView.as_view(), name="circulation_index"),
    path(
        "borrow/<int:book_copy_id>",
        views.BorrowingCreateView.as_view(),
        name="borrowing_add",
    ),
    path(
        "borrow/success",
        TemplateView.as_view(template_name="circulation/borrowing_success.html"),
        name="borrowing_success",
    ),
    path(
        "borrow/<int:pk>/return",
        views.BorrowingReturnView.as_view(),
        name="borrowing_return",
    ),
]
