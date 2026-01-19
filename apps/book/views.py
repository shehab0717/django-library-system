from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.views import View
from .models import Book
from django.urls import reverse
from .froms import AddBookForm, UpdateBookForm, AddBookCopyForm
from django.http import HttpResponseBadRequest, HttpResponseRedirect
from django.db import IntegrityError


class BookListView(View):
    def get(self, request):
        q = request.GET.get("q", "")
        books_queryset = Book.objects.prefetch_related()
        if len(q):
            # search
            books_queryset = Book.objects.prefetch_related().filter(title__icontains=q)
        return render(
            request,
            "book/book_index.html",
            {
                "books": books_queryset.order_by("isbn").all(),
                "q": q,
            },
        )


class BookDetailView(View):
    def get(self, request, book_isbn):
        book = get_object_or_404(Book, pk=book_isbn)
        book_copy_form = AddBookCopyForm()
        return render(
            request,
            "book/book_detail.html",
            context={"book": book, "book_copy_form": book_copy_form},
        )

    def post(self, request, book_isbn):
        book = get_object_or_404(Book, pk=book_isbn)
        book_copy_form = AddBookCopyForm(request.POST)
        if book_copy_form.is_valid():
            print("Form is valid")
            book_copy = book_copy_form.save(commit=False)
            book_copy.book = book
            try:
                book_copy.save()
            except IntegrityError:
                book_copy_form.add_error(
                    field="copy_number", error="This book copy already exists!"
                )
                return render(
                    request,
                    "book/book_detail.html",
                    context={"book": book, "book_copy_form": book_copy_form},
                )
            return HttpResponseRedirect(reverse("book:detail", args=[book_isbn]))


class AddBookView(View):
    def get(self, request):
        form = AddBookForm()
        return render(request, "book/book_add.html", {"form": form})

    def post(self, request):
        form = AddBookForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("book:index"))
        return render(request, "book/book_add.html", {"form": form})


class UpdateBookView(View):
    def get_next_url(self, request):
        return request.GET.get("next", reverse("book:index"))

    def get(self, request, book_isbn):
        book = get_object_or_404(Book, pk=book_isbn)
        form = UpdateBookForm(instance=book)
        return render(
            request,
            "book/book_update.html",
            {
                "form": form,
                "next": self.get_next_url(request),
            },
        )

    def post(self, request, book_isbn):
        book = get_object_or_404(Book, pk=book_isbn)
        form = UpdateBookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(self.get_next_url(request))

        return render(request, "book/book_update.html", {"form": form})


# class BookListView(ListView):
#     model = Book
#     context_object_name = "books"
#     template_name = "book/book_index.html"

#     def get_context_data(self, **kwargs):
#         context_data = super().get_context_data(**kwargs)
#         q = self.request.GET.get("q", "")
#         context_data.update({"q": q})
#         return context_data

#     def get_queryset(self):
#         q = self.request.GET.get("q", "")
#         return Book.objects.prefetch_related().filter(title__icontains=q)


def list(request):
    q = request.GET.get("q", "")
    books_queryset = Book.objects.prefetch_related()
    if len(q):
        # search
        books_queryset = Book.objects.prefetch_related().filter(title__icontains=q)
    return render(
        request,
        "book/book_index.html",
        {"books": books_queryset.order_by("isbn").all(), "q": q},
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
        book_copy_form = AddBookCopyForm(request.POST)
        if book_copy_form.is_valid():
            print("Form is valid")
            book_copy = book_copy_form.save(commit=False)
            book_copy.book = book
            try:
                book_copy.save()
            except IntegrityError:
                book_copy_form.add_error(
                    field="copy_number", error="This book copy already exists!"
                )
                return render(
                    request,
                    "book/book_detail.html",
                    context={"book": book, "book_copy_form": book_copy_form},
                )
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
