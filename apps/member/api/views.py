from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import IsAdminUser

from .serializers import MemberSerializer
from apps.member.models import Member


class MemberListView(ListCreateAPIView):
    serializer_class = MemberSerializer
    queryset = Member.objects.all()
    permission_classes = [IsAdminUser]
