from django.db import models
from django.forms import ValidationError
from apps.core.models import TimestampedModel
from django.utils import timezone

from apps.book.const import BookStatus
from .const import CirculationStatus
from apps.member.models import Member
from apps.book.models import BookCopy


def validate_borrow_date(value: timezone.datetime):
    if timezone.now().date() > value.date():
        raise ValidationError(message="Borrow date cannot be in the future")


class CirculationRecord(TimestampedModel):
    class Status(models.TextChoices):
        ACTIVE = CirculationStatus.ACTIVE, "Active"
        RETURNED = CirculationStatus.RETURNED, "Returned"
        OVERDUE = CirculationStatus.OVERDUE, "Overdue"

    member = models.ForeignKey(
        Member, on_delete=models.CASCADE, related_name="borrowings"
    )
    book_copy = models.ForeignKey(
        BookCopy, on_delete=models.CASCADE, related_name="circulations"
    )
    borrow_date = models.DateTimeField(
        default=timezone.now, validators=[validate_borrow_date]
    )
    due_date = models.DateTimeField()
    return_date = models.DateTimeField(blank=True, null=True)
    status = models.CharField(
        max_length=20, choices=Status.choices, default=CirculationStatus.ACTIVE
    )
    fine = models.IntegerField(default=0, blank=True)

    def save(self, *args, **kwargs):
        self.book_copy.status = (
            BookStatus.BORROWED
            if self.status == CirculationStatus.ACTIVE
            else BookStatus.AVAILABLE
        )
        self.book_copy.save()
        return super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.member} - {self.book_copy}"
