from django.shortcuts import render
from django.shortcuts import get_object_or_404
from .models import Book
from django.urls import reverse
from .froms import AddBookForm, UpdateBookForm, AddBookCopyForm
from django.http import HttpResponseBadRequest, HttpResponseRedirect


def list(request):
    search_text = request.GET.get("book_name", "")
    books_queryset = Book.objects.prefetch_related()
    if len(search_text):
        # search
        books_queryset = Book.objects.prefetch_related().filter(
            title__icontains=search_text
        )
    return render(
        request,
        "book/book_index.html",
        {"books": books_queryset.order_by("isbn").all(), "search_text": search_text},
    )


def get_book(request, book_isbn):
    book = get_object_or_404(Book, pk=book_isbn)
    if request.method == "GET":
        book_copy_form = AddBookCopyForm()
        return render(
            request,
            "book/book_detail.html",
            context={"book": book, "book_copy_form": book_copy_form},
        )
    elif request.method == "POST":
        form = AddBookCopyForm(request.POST)
        if form.is_valid():
            print("Form is valid")
            book_copy = form.save(commit=False)
            book_copy.book = book
            book_copy.save()
            return HttpResponseRedirect(reverse("book:detail", args=[book_isbn]))
    return HttpResponseBadRequest()


def add_book(request):
    if request.method == "GET":
        form = AddBookForm()
        return render(request, "book/book_add.html", {"form": form})
    if request.method == "POST":
        form = AddBookForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("book:index"))
        return render(request, "book/book_add.html", {"form": form})

    return HttpResponseBadRequest()


def update_book(request, book_isbn: int):
    next = request.GET.get("next", reverse("book:index"))
    if request.method == "GET":
        book = get_object_or_404(Book, pk=book_isbn)
        form = UpdateBookForm(instance=book)
        return render(request, "book/book_update.html", {"form": form, "next": next})

    elif request.method == "POST":
        book = get_object_or_404(Book, pk=book_isbn)
        form = UpdateBookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(next)

        return render(request, "book/book_update.html", {"form": form})

    return HttpResponseBadRequest()
