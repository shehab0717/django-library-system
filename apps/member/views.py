from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import View
from . import models
from .forms import MemberCreateForm
from django.contrib.auth.mixins import PermissionRequiredMixin


class MmeberIndexView(PermissionRequiredMixin, View):
    permission_required = "member.view_member"

    def get(self, request):
        members = models.Member.objects.all()
        return render(request, "member/member_index.html", {"members": members})


class MmemberCreateView(PermissionRequiredMixin, View):
    permission_required = "member.add_member"

    def get(self, request):
        form = MemberCreateForm()
        return render(request, "member/member_add.html", {"form": form})

    def post(self, request):
        form = MemberCreateForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("member:member_index"))
        return render(request, "member/member_add.html", {"form": form})


class MemberDetailView(PermissionRequiredMixin, View):
    permission_required = "member.view_member"

    def get(self, request, member_id):
        member = get_object_or_404(models.Member, pk=member_id)
        return render(request, "member/member_detail.html", {"member": member})
