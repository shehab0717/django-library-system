from django.shortcuts import render
from django.shortcuts import get_object_or_404
from .models import Book, Author, Genre
from django.urls import reverse
from .froms import AddBookForm


def list(request):
    books = Book.objects.prefetch_related().all()
    return render(request, "book/index.html", {"books": books})


def get_book(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    return render(request, "book/detail.html", context={"book": book})


def add_book(request):
    form = AddBookForm()
    authors = Author.objects.all()
    genres = Genre.objects.all()
    return render(request, "book/add.html", {"form": form})
