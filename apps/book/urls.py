from django.urls import path
from . import views


app_name = "book"
urlpatterns = [
    # path("", views.list, name="index"),
    path("", views.BookListView.as_view(), name="book_index"),
    path("<int:book_isbn>/", views.BookDetailView.as_view(), name="book_detail"),
    path("<int:book_isbn>/update/", views.UpdateBookView.as_view(), name="book_update"),
    path("add/", views.AddBookView.as_view(), name="book_add"),
]
