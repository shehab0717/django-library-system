from django.db import models
from apps.core.models import TimestampedModel
from apps.book.const import BookStatus


BOOK_STATUS_CHOICES = [
    (BookStatus.AVAILABLE, "Available"),
    (BookStatus.BORROWED, "Borrowed"),
    (BookStatus.MAINTAINANCE, "Under Maintainance"),
]


class Book(TimestampedModel):
    isbn = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=200)
    pub_year = models.IntegerField("publish year")
    genres = models.ManyToManyField("Genre")

    @property
    def is_available(self):
        return self.bookcopy_set.filter(status=BookStatus.AVAILABLE).count() > 0

    def __str__(self):
        return self.title


class BookCopy(TimestampedModel):
    copy_number = models.IntegerField("copy number")
    status = models.CharField(max_length=20, choices=BOOK_STATUS_CHOICES)
    book = models.ForeignKey(Book, on_delete=models.CASCADE, db_column="book_isbn")

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=("copy_number", "book"),
                name="unique-copy-per-book-constraint",
            )
        ]

    def __str__(self):
        return f"{self.book.title}({self.copy_number})"


class Genre(TimestampedModel):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name
