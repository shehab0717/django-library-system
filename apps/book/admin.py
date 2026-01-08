from django.contrib import admin
from apps.book.models import Book, BookCopy, Genre, Author

# Register your models here.
admin.site.register([Book, BookCopy, Genre, Author])
