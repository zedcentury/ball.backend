from django.contrib import admin
from django.urls import path, include

from notification.views import index

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('user.urls')),
    path('', include('common.urls')),
    path('', include('account.urls')),
    path('', include('score.urls')),
    path('notification/', index)
]
