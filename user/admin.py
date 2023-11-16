from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from user.models import User, Pupil

admin.site.register(User, UserAdmin)
admin.site.register(Pupil)
