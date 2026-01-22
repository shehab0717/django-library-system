from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.views import View
from .models import Book, Author, BookImage, Genre
from django.urls import reverse
from . import forms
from django.http import HttpResponseRedirect
from django.db import IntegrityError
from django.db.models import Q
from django.forms import inlineformset_factory


class BookListView(View):
    def get(self, request):
        q = request.GET.get("q", "")
        all_books = Book.objects.filter(title__icontains=q).all()
        filters = self._get_filters(all_books)
        f = self._genre_filter & self._author_filter
        filtered_books = (
            all_books.filter(f).distinct().select_related().order_by("isbn").all()
        )
        return render(
            request,
            "book/book_index.html",
            {"books": filtered_books, "q": q, "filters": filters},
        )

    @property
    def _genre_filter(self):
        selected_genres = self.request.GET.getlist("genre", [])
        return Q(genres__id__in=selected_genres) if selected_genres else Q()

    @property
    def _author_filter(self):
        selected_authors = self.request.GET.getlist("author", [])
        return Q(authors__id__in=selected_authors) if selected_authors else Q()

    def _get_filters(self, books_queryset):
        selected_genres = self.request.GET.getlist("genre", [])
        selected_authors = self.request.GET.getlist("author", [])

        genres = Genre.objects.filter(books__in=books_queryset).distinct()
        authors = Author.objects.filter(books__in=books_queryset).distinct()

        for g in genres:
            g.selected = str(g.id) in selected_genres

        for a in authors:
            a.selected = str(a.id) in selected_authors

        return {"genres": genres, "authors": authors}


class BookDetailView(View):
    def get(self, request, book_isbn):
        book = get_object_or_404(Book, pk=book_isbn)
        book_copy_form = forms.BookCopyCreateForm()
        return render(
            request,
            "book/book_detail.html",
            context={"book": book, "book_copy_form": book_copy_form},
        )

    def post(self, request, book_isbn):
        book = get_object_or_404(Book, pk=book_isbn)
        book_copy_form = forms.BookCopyCreateForm(request.POST)
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
    BookImageFormSet = inlineformset_factory(
        Book,
        BookImage,
        fields=("image",),
        extra=3,
    )

    def get(self, request):
        images_formset = self.BookImageFormSet()
        form = forms.BookCreateForm()
        return render(
            request,
            "book/book_add.html",
            {"form": form, "images_formset": images_formset},
        )

    def post(self, request):
        form = forms.BookCreateForm(request.POST, request.FILES)
        book = Book()
        images_formset = self.BookImageFormSet(
            request.POST, request.FILES, instance=book
        )
        if form.is_valid() and images_formset.is_valid():
            book = form.save()
            images_formset.instance = book
            images_formset.save()
            return HttpResponseRedirect(reverse("book:book_index"))
        return render(
            request,
            "book/book_add.html",
            {"form": form, "images_formset": images_formset},
        )


class UpdateBookView(View):
    def get_next_url(self, request):
        return request.GET.get("next", reverse("book:book_index"))

    def get(self, request, book_isbn):
        book = get_object_or_404(Book, pk=book_isbn)
        form = forms.UpdateBookForm(instance=book)
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
        form = forms.UpdateBookForm(request.POST, request.FILES, instance=book)
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
        list_view = request.GET.get("view", "grid")
        query = Q(name__icontains=q) | Q(bio__icontains=q)
        authors = Author.objects.filter(query).order_by("name").all()
        return render(
            request,
            "book/author_index.html",
            {"authors": authors, "q": q, "view": list_view},
        )


class AuthorCreateView(View):
    def get(self, request):
        form = forms.AuthorCreateForm()
        return render(request, "book/author_add.html", {"form": form})

    def post(self, request):
        form = forms.AuthorCreateForm(request.POST, request.FILES)
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


class AuthorUpdateView(View):
    def get(self, request, author_id):
        author = get_object_or_404(Author, pk=author_id)
        form = forms.AuthorUpdateForm(instance=author)
        return render(request, "book/author_update.html", {"form": form})

    def post(self, request, author_id):
        author = get_object_or_404(Author, pk=author_id)
        form = forms.AuthorUpdateForm(request.POST, request.FILES, instance=author)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("book:author_detail", args=[author_id]))
        return render(request, "book/author_update.html", {"form": form})


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
