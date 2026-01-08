from django.contrib import admin
from .models import Member, Membership
# Register your models here.

admin.site.register([Member, Membership])
