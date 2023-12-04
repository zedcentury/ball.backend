from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from user.models import User, Pupil, Teacher, Parent

admin.site.register(User, UserAdmin)
admin.site.register(Teacher)
admin.site.register(Parent)
admin.site.register(Pupil)
