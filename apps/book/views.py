from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.views import View
from .models import Book, Author
from django.urls import reverse
from .froms import AddBookForm, UpdateBookForm, AddBookCopyForm, AddAuthorForm
from django.http import HttpResponseRedirect
from django.db import IntegrityError
from django.db.models import Q


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
            return HttpResponseRedirect(reverse("book:book_detail", args=[book_isbn]))


class AddBookView(View):
    def get(self, request):
        form = AddBookForm()
        return render(request, "book/book_add.html", {"form": form})

    def post(self, request):
        form = AddBookForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("book:book_index"))
        return render(request, "book/book_add.html", {"form": form})


class UpdateBookView(View):
    def get_next_url(self, request):
        return request.GET.get("next", reverse("book:book_index"))

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


class DeleteBookView(View):
    def post(self, request, book_isbn):
        book = get_object_or_404(Book, pk=book_isbn)
        book.delete()
        return HttpResponseRedirect(reverse("book:book_index"))


class AuthorListView(View):
    def get(self, request):
        q = request.GET.get("q", "")
        query = Q(name__icontains=q) | Q(bio__icontains=q)
        authors = Author.objects.filter(query).all()
        return render(request, "book/author_index.html", {"authors": authors, "q": q})


class AuthorCreateView(View):
    def get(self, request):
        form = AddAuthorForm()
        return render(request, "book/author_add.html", {"form": form})

    def post(self, request):
        form = AddAuthorForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("book:author_index"))

        return render(request, "book/author_add.html", {"form": form})


class AuthorDetailview(View):
    def get(self, request, author_id):
        author = get_object_or_404(
            Author.objects.prefetch_related("books"), pk=author_id
        )
        return render(request, "book/author_detail.html", {"author": author})


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
