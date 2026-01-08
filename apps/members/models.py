from django.db import models
from apps.core.models import TimestampedModel
from apps.members.const import MemberStatus


class Member(TimestampedModel):
    class Status(models.TextChoices):
        ACTIVE = MemberStatus.active, "Active"
        SUSPENDED = MemberStatus.suspended, "Suspended"
        EXPIRED = MemberStatus.expired, "Expired"

    name = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=14)
    email = models.CharField(max_length=50, blank=True, null=True)
    membership = models.ForeignKey("Membership", on_delete=models.CASCADE)
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.ACTIVE,
    )

    def __str__(self):
        return self.name


class Membership(TimestampedModel):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name
