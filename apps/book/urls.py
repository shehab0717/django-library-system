from django.urls import path
from . import views


app_name = "book"
urlpatterns = [
    # Books
    path("", views.BookListView.as_view(), name="book_index"),
    path("<int:book_isbn>/", views.BookDetailView.as_view(), name="book_detail"),
    path("<int:book_isbn>/update/", views.UpdateBookView.as_view(), name="book_update"),
    path("<int:book_isbn>/delete/", views.DeleteBookView.as_view(), name="book_delete"),
    path("add/", views.AddBookView.as_view(), name="book_add"),
    # Authors
    path("author/", views.AuthorListView.as_view(), name="author_index"),
    path("author/add/", views.AuthorCreateView.as_view(), name="author_add"),
    path(
        "author/<int:author_id>/detail/",
        views.AuthorDetailview.as_view(),
        name="author_detail",
    ),
    path(
        "author/<int:author_id>/update/",
        views.AuthorUpdateView.as_view(),
        name="author_update",
    ),
]
