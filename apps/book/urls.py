from django.urls import path
from . import views


app_name = "book"
urlpatterns = [
    path("", views.list, name="index"),
    path("<int:book_isbn>/", views.get_book, name="detail"),
    path("<int:book_isbn>/update/", views.update_book, name="update"),
    path("add/", views.add_book, name="add"),
]
