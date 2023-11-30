from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('user.urls')),
    path('', include('common.urls')),
    path('', include('account.urls')),
    path('', include('score.urls'))
]
