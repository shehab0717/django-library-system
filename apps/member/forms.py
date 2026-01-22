from django.forms import ModelForm
from .models import Member


class MemberCreateForm(ModelForm):
    class Meta:
        model = Member
        fields = "__all__"
