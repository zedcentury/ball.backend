from django.contrib import admin

from common.models import ClassName

@admin.register(ClassName)
class ClassNameAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')

    # class Meta:
    #     model = ClassName


# admin.site.register(ClassName)
