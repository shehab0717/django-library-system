from django.urls import path
from . import views


app_name = "book"
urlpatterns = [
    # path("", views.list, name="index"),
    path("", views.BookListView.as_view(), name="index"),
    path("<int:book_isbn>/", views.BookDetailView.as_view(), name="detail"),
    path("<int:book_isbn>/update/", views.UpdateBookView.as_view(), name="update"),
    path("add/", views.AddBookView.as_view(), name="add"),
]
