from datetime import timedelta
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import View
from django.http import HttpResponseBadRequest

from .const import CirculationStatus

from .models import CirculationRecord
from .forms import BorrowingCreateForm

from django.utils import timezone

from apps.book.models import BookCopy


class CirculationIndexView(View):
    def get(self, request):
        return render(request, "circulation/circulation_index.html", {})


class BorrowingCreateView(View):
    def get(self, request, book_copy_id):
        book_copy = get_object_or_404(BookCopy, pk=book_copy_id)
        if not book_copy.is_available():
            return HttpResponseBadRequest(
                "This book copy is not available, it is already borrowed"
            )
        form = BorrowingCreateForm()
        return render(
            request,
            "circulation/borrowing_add.html",
            {"book_copy": book_copy, "form": form},
        )

    def post(self, request, book_copy_id):
        book_copy = get_object_or_404(BookCopy, pk=book_copy_id)
        if not book_copy.is_available():
            return HttpResponseBadRequest(
                "This book copy is not available, it is already borrowed"
            )
        form = BorrowingCreateForm(request.POST)
        if form.is_valid():
            circulation: CirculationRecord = form.save(commit=False)
            circulation.due_date = timezone.now().date() + timedelta(
                int(form.cleaned_data["period"])
            )
            circulation.book_copy = book_copy
            circulation.save()
            return HttpResponseRedirect(reverse("circulation:borrowing_success"))
        return render(
            request,
            "circulation/borrowing_add.html",
            {"book_copy": book_copy, "form": form},
        )


class BorrowingReturnView(View):
    def post(self, request, pk):
        circulation_record = get_object_or_404(CirculationRecord, pk=pk)
        next = request.GET.get(
            "next", reverse("member:member_detail", args=[circulation_record.member.id])
        )
        circulation_record.status = CirculationStatus.RETURNED
        circulation_record.return_date = timezone.now()

        circulation_record.save()
        return HttpResponseRedirect(next)
