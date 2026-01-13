from django.urls import path
from . import views


app_name = "book"
urlpatterns = [
    path("", views.list, name="index"),
    path("detail/<int:book_id>", views.get_book, name="detail"),
]
