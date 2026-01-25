from django.shortcuts import render
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.


class UserProfileView(LoginRequiredMixin, View):
    def get(self, request):
        user = request.user
        return render(request, "accounts/profile.html", {"user": user})
