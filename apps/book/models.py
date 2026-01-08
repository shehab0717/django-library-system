from django.db import models
from django.forms import ValidationError
from apps.core.models import TimestampedModel
from apps.book.const import BookStatus


class Book(TimestampedModel):
    isbn = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=200)
    pub_year = models.IntegerField("publish year")
    genres = models.ManyToManyField("Genre", related_name="books")
    authors = models.ManyToManyField("Author", related_name="books")

    @property
    def is_available(self):
        return self.bookcopy_set.filter(status=BookStatus.AVAILABLE).count() > 0

    def __str__(self):
        return self.title


class BookCopy(TimestampedModel):
    class Status(models.TextChoices):
        AVAILABLE = BookStatus.AVAILABLE, "Available"
        BORROWED = BookStatus.BORROWED, "Borrowed"
        MAINTAINANCE = BookStatus.MAINTAINANCE, "Under Maintainance"

    copy_number = models.IntegerField("copy number")
    status = models.CharField(max_length=20, choices=Status.choices)
    book = models.ForeignKey(Book, on_delete=models.CASCADE, db_column="book_isbn")

    class Meta:
        verbose_name_plural = "Book copies"
        constraints = [
            models.UniqueConstraint(
                fields=("copy_number", "book"),
                name="unique-copy-per-book-constraint",
            )
        ]

    def __str__(self):
        return f"{self.book.title}({self.copy_number})"


class Genre(TimestampedModel):
    name = models.CharField(max_length=20)

    def delete(self, *args, **kwargs):
        for book in self.books.all():
            if book.genres.count() == 1:
                raise ValidationError(
                    f'Cannot delete genre "{self.name}" because '
                    f'"{book.title}" would have no genres.'
                )
        super().delete(*args, **kwargs)

    def __str__(self):
        return self.name


class Author(TimestampedModel):
    name = models.CharField(max_length=50)
    bio = models.CharField(max_length=400)
    nationality = models.CharField(max_length=50)
    birth_date = models.DateField()
    death_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.name} - {self.nationality}"
