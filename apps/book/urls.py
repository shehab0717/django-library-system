from django.urls import path
from . import views


app_name = "book"
urlpatterns = [
    path("", views.list, name="index"),
    path("<int:book_id>/", views.get_book, name="detail"),
    path("add/", views.add_book, name="add"),
]
