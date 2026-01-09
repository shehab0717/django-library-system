from django.db import models
from apps.core.models import TimestampedModel
from django.utils import timezone
from .const import CirculationStatus
from apps.members.models import Member
from apps.book.models import BookCopy


class CirculationRecord(TimestampedModel):
    class Status(models.TextChoices):
        ACTIVE = CirculationStatus.ACTIVE, "Active"
        RETURNED = CirculationStatus.RETURNED, "Returned"
        OVERDUE = CirculationStatus.OVERDUE, "Overdue"

    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    book_copy = models.ForeignKey(BookCopy, on_delete=models.CASCADE)
    borrow_date = models.DateTimeField(default=timezone.now())
    due_date = models.DateTimeField()
    status = models.CharField(max_length=20, choices=Status.choices)
    fine = models.IntegerField(default=0, blank=True)

    def __str__(self):
        return f"{self.member} - {self.book_copy}"
