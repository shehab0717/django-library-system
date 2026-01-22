from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views import View
from . import models
from .forms import MemberCreateForm


class MmeberIndexView(View):
    def get(self, request):
        members = models.Member.objects.all()
        return render(request, "member/member_index.html", {"members": members})


class MmemberCreateView(View):
    def get(self, request):
        form = MemberCreateForm()
        return render(request, "member/member_add.html", {"form": form})

    def post(self, request):
        form = MemberCreateForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("member:member_index"))
        return render(request, "member/member_add.html", {"form": form})
